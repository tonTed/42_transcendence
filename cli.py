import asyncio
import json
import requests
import websockets
import ssl
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PongGameClient:
    def __init__(self, jwt_token):
        self.jwt_token = jwt_token
        self.game_id = None
        self.state = {}

    def create_game(self):
        self.ended = False
        url = "http://localhost/api/games/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.jwt_token,
        }
        data = {"players": [{"id": None, "name": "cli1"}, {"id": None, "name": "cli2"}]}

        try:
            print("Sending POST request to:", url)
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            game_info = response.json()
            print("GAME INFO:")
            print(game_info)
            self.game_id = game_info["id"]
            return self.game_id

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")

        return None

    async def connect_to_game(self):
        if not self.game_id:
            print("No game ID found. Please create a game first.")
            return

        ws_url = f"wss://localhost/ws/game/?game_id={self.game_id}&jwt={self.jwt_token}"
        ssl_context = ssl._create_unverified_context()

        try:
            async with websockets.connect(ws_url, ssl=ssl_context) as websocket:
                await asyncio.gather(
                    self.handle_server_messages(websocket),
                    self.get_user_input(websocket),
                )
        except websockets.InvalidURI:
            print("Invalid WebSocket URI. Please check the server address.")
        except websockets.InvalidHandshake:
            print("Invalid WebSocket handshake. Please verify your JWT token.")
        except websockets.ConnectionClosedError as e:
            print(f"WebSocket connection closed with error: {e}")
        except ssl.SSLError as ssl_err:
            print(f"SSL error occurred: {ssl_err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    async def handle_server_messages(self, websocket):
        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)

                if "state" in data:
                    self.state = data["state"]
                elif "final" in data:
                    self.state = data["final"]
                    self.ended = True
                    break

        except websockets.ConnectionClosedError:
            print("Connection closed")
        except websockets.ConnectionClosedOK:
            print("Connection closed normally.")
        except Exception as e:
            print(f"An error occurred while receiving a message: {e}")
        finally:
            self.ended = True
            await websocket.close()

    async def get_user_input(self, websocket):
        await asyncio.sleep(0.5)

        actions = {
            "p1Up": False,
            "p1Down": False,
            "p2Up": False,
            "p2Down": False,
        }

        while True:
            user_input = (
                input("\nEnter command ('w', 's', 'u', 'd', 'state', or 'quit'): ")
                .strip()
                .lower()
            )
            await asyncio.sleep(0.1)

            if user_input == "quit":
                print("Quitting game")
                self.ended = True
                await websocket.close()
                break

            if user_input == "state":
                if not self.ended:
                    self.print_state()

            elif user_input == "w":
                actions["p1Up"] = True
                actions["p1Down"] = False

            elif user_input == "s":
                actions["p1Down"] = True
                actions["p1Up"] = False

            elif user_input == "u":
                actions["p2Up"] = True
                actions["p2Down"] = False

            elif user_input == "d":
                actions["p2Down"] = True
                actions["p2Up"] = False

            else:
                print("Unknown command")

            action_message = json.dumps({"command": "actions", "actions": actions})
            try:
                await websocket.send(action_message)

                actions = {
                    "p1Up": False,
                    "p1Down": False,
                    "p2Up": False,
                    "p2Down": False,
                }

                action_message = json.dumps({"command": "actions", "actions": actions})
                await websocket.send(action_message)

            except websockets.ConnectionClosed:
                self.ended = True
                self.print_state()
                print("\nConnection Closed")
                break

            await asyncio.sleep(0.1)

    def print_state(self):
        if self.ended is False:
            print("\n--- Game State Update ---")
            print(f"Ball Position: {self.state['ball_position']}")
            print(f"Player 1 Paddle: {self.state['paddle1_position']}")
            print(f"Player 2 Paddle: {self.state['paddle2_position']}")
            print(f"Scores: {self.state['scores']}")
        else:
            print("\n--- Game Over ---")
            print(f"Final Scores: {self.state['scores']}")
            print(f"Winner: Player {self.state['winner']}")

def verify_token(jwt_token) -> bool:
    url = "http://localhost/api/auth/verify/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": jwt_token,
    }

    try:
        response = requests.post(url, headers=headers, verify=False)
        response.raise_for_status()

        data = response.json()
        if data.get("valid"):
            return True
        else:
            print(f"Token verification failed: {data}")
            return False
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return False


def main():
    jwt_token = input("Enter your JWT token: ")

    if verify_token(jwt_token=jwt_token) is False:
        print("\nToken invalid. Exiting program")
        exit()
    
    client = PongGameClient(jwt_token)

    while True:
        print("\n--- Main Menu ---")
        print("1. Create Game")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            print(
                "'w'/'s' to move player 1 | 'u'/'d' to move player 2 | 'state' to get "
                "the game state | 'quit' to quit"
            )
            input("Press ENTER to start the game")
            game_id = client.create_game()
            if game_id:
                print(f"Game created successfully with ID: {game_id}")
                asyncio.run(client.connect_to_game())
            else:
                print("Failed to create game. Please try again.")

        elif choice == "2":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()

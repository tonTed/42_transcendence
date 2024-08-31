import asyncio
import json
import requests
import websockets
import ssl

class PongGameClient:
    def __init__(self, jwt_token):
        self.jwt_token = jwt_token
        self.game_id = None
        self.state = {}
        self.ended = False

    def create_game(self):
        url = "http://localhost/api/games/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.jwt_token,
        }
        data = {
            "players": [
                {"id": None, "name": 'cli1'},
                {"id": None, "name": 'cli2'}
            ]
        }
        
        print("Sending POST request to:", url)
        response = requests.post(url, headers=headers, json=data, verify=False)
        print(response.status_code)
        if response.status_code == 200:
            game_info = response.json()
            print('GAME INFO:')
            print(game_info)
            self.game_id = game_info["id"]
            return self.game_id
        else:
            print("Error creating game:", response.status_code, response.text)
            return None

    async def connect_to_game(self):
        if not self.game_id:
            print("No game ID found. Please create a game first.")
            return

        ws_url = f"wss://localhost/ws/game/?game_id={self.game_id}&jwt={self.jwt_token}"
        ssl_context = ssl._create_unverified_context()
        async with websockets.connect(ws_url, ssl=ssl_context) as websocket:
            await asyncio.gather(
                self.handle_server_messages(websocket),
                self.get_user_input(websocket)
            )

    async def handle_server_messages(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                
                if 'state' in data:
                    self.state = data['state']
                elif 'final' in data:
                    self.state = data['final']
                    self.ended = True
                    break
            
            except websockets.ConnectionClosed:
                print("Connection closed unexpectedly")
                print("Exiting program...")
                exit()

    async def get_user_input(self, websocket):
        await asyncio.sleep(0.5)
        
        actions = {
            "p1Up": False,
            "p1Down": False,
            "p2Up": False,
            "p2Down": False,
        }

        while True:
            user_input = input("\nEnter command ('w', 's', 'u', 'd', 'state', or 'quit'): ").strip().lower()
            await asyncio.sleep(0.1)
            
            if user_input == 'quit':
                print("Quitting game and exiting program")
                exit()

            if user_input == 'state':
                self.print_state()

            elif user_input == 'w':
                actions["p1Up"] = True
                actions["p1Down"] = False

            elif user_input == 's':
                actions["p1Down"] = True
                actions["p1Up"] = False

            elif user_input == 'u':
                actions["p2Up"] = True
                actions["p2Down"] = False

            elif user_input == 'd':
                actions["p2Down"] = True
                actions["p2Up"] = False
            
            else:
                print('Unknown command')

            action_message = json.dumps({
                "command": "actions",
                "actions": actions
            })
            try:
                await websocket.send(action_message)

                actions = {
                    "p1Up": False,
                    "p1Down": False,
                    "p2Up": False,
                    "p2Down": False,
                }

                action_message = json.dumps({
                    "command": "actions",
                    "actions": actions
                })
                await websocket.send(action_message)

            except websockets.ConnectionClosed:
                self.print_state()
                print('\nConnection Closed')
                print("Exiting program...")
                exit()

            await asyncio.sleep(0.1)

    def print_state(self):
        if 'ball_position' in self.state:
            print("\n--- Game State Update ---")
            print(f"Ball Position: {self.state['ball_position']}")
            print(f"Player 1 Paddle: {self.state['paddle1_position']}")
            print(f"Player 2 Paddle: {self.state['paddle2_position']}")
            print(f"Scores: {self.state['scores']}")
        else:
            print("\n--- Game Over ---")
            print(f"Final Scores: {self.state['scores']}")
            print(f"Winner: Player {self.state['winner']}")

def main():
    jwt_token = input("Enter your JWT token: ")

    client = PongGameClient(jwt_token)

    while True:
        print("\n--- Main Menu ---")
        print("1. Create Game")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            print("'w'/'s' to move player 1 | 'u'/'d' to move player 2 | 'state' to get the game state | 'quit' to quit")
            input("Press any key to start the game")
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

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

    def create_game(self, player1_name, player2_name):
        url = "http://localhost/api/games/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.jwt_token,
        }
        data = {
            "players": [
                {"id": None, "name": player1_name},
                {"id": None, "name": player2_name}
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
                self.get_user_input()
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
                break

    async def get_user_input(self):
        await asyncio.sleep(0.5)

        while self.ended is False:
            user_input = input("\nEnter command (type 'state' to view state): ")
            await asyncio.sleep(0.1)
            if user_input == 'state':
                self.print_state()
            
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
            player1_name = input("Enter player1 name: ")
            player2_name = input("Enter player2 name: ")
            game_id = client.create_game(player1_name, player2_name)
            
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

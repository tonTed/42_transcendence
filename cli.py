import requests
import argparse
import asyncio
import websockets
import json

# Fonction pour créer une partie
def create_game(player1_name, player2_name, jwt_token):
    url = "http://localhost/api/games/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": jwt_token,
    }
    data = {
        "players": [
            {"id": 12, "name": player1_name},
            {"id": 11, "name": player2_name}
        ]
    }
    
    print("Sending POST request to:", url)
    # response = requests.post(url, headers=headers, json=data, verify=False)
    response = requests.post(url, headers=headers, json=json.dumps(data), verify=False)
    print(response.status_code)
    if response.status_code == 200:
        game_info = response.json()
        print('GAME INFO:')
        print(game_info)
        return game_info["id"]  # Retourne l'ID du jeu créé
    else:
        print("Erreur lors de la création du jeu:", response.status_code, response.text)
        return None

# Fonction pour se connecter au jeu via WebSocket
async def connect_to_game(game_id, jwt_token):
    ws_url = f"ws://localhost:8000/ws/game/?game_id={game_id}&jwt={jwt_token}"
    async with websockets.connect(ws_url) as websocket:
        await game_loop(websocket)

async def game_loop(websocket):
    print("Connected to the game. Waiting for game updates...")
    while True:
        try:
            # Recevoir les mises à jour du jeu depuis le serveur
            message = await websocket.recv()
            data = json.loads(message)
            
            if 'state' in data:
                print("\n--- Game State Update ---")
                print(f"Ball Position: {data['state']['ball_position']}")
                print(f"Player 1 Paddle: {data['state']['paddle1_position']}")
                print(f"Player 2 Paddle: {data['state']['paddle2_position']}")
                print(f"Scores: {data['state']['scores']}")
            
            elif 'final' in data:
                print("\n--- Game Over ---")
                print(f"Final Scores: {data['final']['scores']}")
                print(f"Winner: Player {data['final']['winner']}")
                break
            
            # Exemple pour envoyer une commande pour déplacer la raquette
            user_input = input("\nEnter command (w/s for up/down, p to pause): ")
            if user_input in ['w', 's']:
                actions = {'move': 'up' if user_input == 'w' else 'down'}
                await websocket.send(json.dumps({'command': 'actions', 'actions': actions}))
            elif user_input == 'p':
                await websocket.send(json.dumps({'command': 'pause'}))
        
        except websockets.ConnectionClosed:
            print("Connection closed")
            break

# Fonction principale du menu CLI
def main():
    jwt_token = input("Enter your JWT token: ")

    while True:
        print("\n--- Main Menu ---")
        print("1. Create Game")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            player1_name = input("Enter player1 name: ")
            player2_name = input("Enter player2 name: ")
            game_id = create_game(player1_name, player2_name, jwt_token)
            
            if game_id:
                print(f"Game created successfully with ID: {game_id}")
                asyncio.run(connect_to_game(game_id, jwt_token))
            else:
                print("Failed to create game. Please try again.")
        
        elif choice == "2":
            print("Exiting program...")
            break
        
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()

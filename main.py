import time

# Initialize game variables
game_state = {1: ' ', 2: ' ', 3: ' ', 4: ' ', 5: ' ', 6: ' ', 7: ' ', 8: ' ', 9: ' '}
player_dict = {"Name": "Player", "Symbol": "X"}
ai_dict = {"Name": "AI", "Symbol": "O"}
game_history = []
game_stats = {"games_played": 0, "player_wins": 0, "ai_wins": 0, "draws": 0}

# Define AI players
ai_players = [
    {"Name": "Juan Gonzalez", "Difficulty": "easy"},
    {"Name": "Bobby Fresh", "Difficulty": "normal"},
    {"Name": "Jethroe Gillmore", "Difficulty": "hard"}
]


def print_game_board(state):
    board = f" {state[1]} | {state[2]} | {state[3]} \n" \
            "___________\n" \
            f" {state[4]} | {state[5]} | {state[6]} \n" \
            "___________\n" \
            f" {state[7]} | {state[8]} | {state[9]} "
    print(board)


def check_winner(state):
    winning_combinations = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Rows
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Columns
        (1, 5, 9), (3, 5, 7)  # Diagonals
    ]
    for combo in winning_combinations:
        if state[combo[0]] == state[combo[1]] == state[combo[2]] != ' ':
            if state[combo[0]] == player_dict["Symbol"]:
                return player_dict["Name"]
            else:
                return ai_dict["Name"]
    if all(state[pos] != ' ' for pos in range(1, 10)):
        return 'Draw'
    return None


def minimax(state, depth, is_maximizing, alpha, beta):
    result = check_winner(state)
    if result == player_dict["Name"]:
        return -1
    elif result == ai_dict["Name"]:
        return 1
    elif result == "Draw":
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for key in state.keys():
            if state[key] == " ":
                state[key] = ai_dict["Symbol"]
                score = minimax(state, depth + 1, False, alpha, beta)
                state[key] = " "
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float("inf")
        for key in state.keys():
            if state[key] == " ":
                state[key] = player_dict["Symbol"]
                score = minimax(state, depth + 1, True, alpha, beta)
                state[key] = " "
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score


def get_ai_move(difficulty):
    best_score = -float("inf")
    best_move = None
    for key in game_state.keys():
        if game_state[key] == " ":
            game_state[key] = ai_dict["Symbol"]
            score = minimax(game_state, 0, False, -float("inf"), float("inf"))
            game_state[key] = " "
            if score > best_score:
                best_score = score
                best_move = key
            if difficulty == "easy" and best_score > 0:
                break
    return best_move


def make_move(player, position):
    game_state[position] = player["Symbol"]
    game_history.append((player["Name"], position))


def reset_game():
    global game_state, game_history
    game_state = {1: ' ', 2: ' ', 3: ' ', 4: ' ', 5: ' ', 6: ' ', 7: ' ', 8: ' ', 9: ' '}
    game_history = []


def update_stats(winner):
    game_stats["games_played"] += 1
    if winner == player_dict["Name"]:
        game_stats["player_wins"] += 1
    elif winner == ai_dict["Name"]:
        game_stats["ai_wins"] += 1
    else:
        game_stats["draws"] += 1


def display_stats():
    print("Game Statistics:")
    print(f"Games Played: {game_stats['games_played']}")
    print(f"{player_dict['Name']} Wins: {game_stats['player_wins']}")
    print(f"{ai_dict['Name']} Wins: {game_stats['ai_wins']}")
    print(f"Draws: {game_stats['draws']}")


def play_game(ai_player):
    global ai_dict
    ai_dict["Name"] = ai_player["Name"]
    difficulty = ai_player["Difficulty"]
    print(f"\nPlaying against {ai_dict['Name']}. Let the battle begin!\n")

    while True:
        print_game_board(game_state)
        while True:
            try:
                position = int(input(f"{player_dict['Name']}, enter a position (1-9): "))
                if position in range(1, 10) and game_state[position] == ' ':
                    make_move(player_dict, position)
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        winner = check_winner(game_state)
        if winner:
            print_game_board(game_state)
            if winner == "Draw":
                print("It's a draw!")
            else:
                print(f"{winner} wins!")
            update_stats(winner)
            break

        print(f"\n{ai_dict['Name']} is thinking...\n")
        time.sleep(3)
        ai_move = get_ai_move(difficulty)
        make_move(ai_dict, ai_move)

        winner = check_winner(game_state)
        if winner:
            print_game_board(game_state)
            if winner == "Draw":
                print("It's a draw!")
            else:
                print(f"{winner} wins!")
            update_stats(winner)
            break


def main_menu():
    while True:
        print("\nWelcome to Tic Tac Toe!")
        print("1. Play against AI")
        print("2. Customize Player Symbol")
        print("3. View Game Statistics")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            ai_menu()
        elif choice == "2":
            customize_player()
        elif choice == "3":
            display_stats()
        elif choice == "4":
            print("Thanks for playing. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def ai_menu():
    while True:
        print("\nChoose an AI opponent:")
        for i, ai in enumerate(ai_players, 1):
            print(f"{i}. {ai['Name']}")
        print(f"{len(ai_players) + 1}. Go back")

        choice = input("Enter your choice (1-4): ")

        if choice.isdigit() and 1 <= int(choice) <= len(ai_players):
            ai_player = ai_players[int(choice) - 1]
            play_game(ai_player)

            if ai_player != ai_players[-1]:
                play_again = input("Do you want to play against a tougher opponent? (y/n): ")
                if play_again.lower() == "y":
                    continue
                else:
                    break
            else:
                break
        elif choice == str(len(ai_players) + 1):
            break
        else:
            print("Invalid choice. Please try again.")


def customize_player():
    symbol = input("Enter a new symbol for the player: ")
    player_dict["Symbol"] = symbol
    print(f"Player symbol updated to '{symbol}'.")
    time.sleep(2)


# Start the game
if __name__ == "__main__":
    main_menu()

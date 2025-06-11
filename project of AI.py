
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class TicTacToe:
    def _init_(self):
        self.board = ['1','2','3','4','5','6','7','8','9']
        self.current_player = "User"

    def draw_board(self):
        print("\n" * 5)
        print("=== Tic Tac Toe Game (User vs AI) ===\n")
        for i in range(3):
            print(" " + self.board[3*i] + " | " + self.board[3*i+1] + " | " + self.board[3*i+2])
            if i < 2:
                print("---|---|---")
        self.draw_visual_board()

    def draw_visual_board(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')
        plt.title(f"{self.current_player}'s Turn", fontsize=14)

        for row in range(3):
            for col in range(3):
                idx = 3 * (2 - row) + col
                mark = self.board[idx]
                ax.add_patch(patches.Rectangle((col, row), 1, 1, fill=False, edgecolor='black'))
                color = 'blue' if mark == 'X' else ('red' if mark == 'O' else 'gray')
                ax.text(col + 0.5, row + 0.5, mark, ha='center', va='center', fontsize=36, color=color)

        plt.pause(0.3)
        plt.close()

    def switch_player(self):
        self.current_player = "AI" if self.current_player == "User" else "User"

    def mark_board(self, pos, mark):
        if self.board[pos] in ['X', 'O']:
            return False
        self.board[pos] = mark
        return True

    def check_winner(self, board=None):
        board = board or self.board
        winning_combinations = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]]:
                return board[combo[0]]
        return None

    def is_draw(self, board=None):
        board = board or self.board
        return all(cell in ['X', 'O'] for cell in board) and not self.check_winner(board)

    def get_available_moves(self, board):
        return [i for i in range(9) if board[i] not in ['X', 'O']]

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        winner = self.check_winner(board)
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif self.is_draw(board):
            return 0

        if is_maximizing:
            max_eval = -float('inf')
            for move in self.get_available_moves(board):
                board_copy = board[:]
                board_copy[move] = 'O'
                eval = self.minimax(board_copy, depth + 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_available_moves(board):
                board_copy = board[:]
                board_copy[move] = 'X'
                eval = self.minimax(board_copy, depth + 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_ai_move(self):
        best_score = -float('inf')
        best_move = None
        for move in self.get_available_moves(self.board):
            board_copy = self.board[:]
            board_copy[move] = 'O'
            score = self.minimax(board_copy, 0, False, -float('inf'), float('inf'))
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def reset_game(self):
        self.board = ['1','2','3','4','5','6','7','8','9']
        self.current_player = "User"

    def get_user_input(self):
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if move in range(9):
                return move
            else:
                print("Invalid number! Please enter between 1 and 9.")
                return None
        except ValueError:
            print("Invalid input! Please enter a number.")
            return None

    def display_winner(self):
        self.draw_board()
        winner = self.check_winner()
        if winner == 'X':
            print("🎉 You win! Great job!")
        elif winner == 'O':
            print("😔 AI wins! Better luck next time.")
        else:
            print("It's a draw!")

    def ask_to_play_again(self):
        while True:
            print("\nDo you want to play again?")
            print("1. Yes")
            print("2. No")
            choice = input("Enter choice (1 or 2): ").strip()
            if choice == '1':
                return True
            elif choice == '2':
                return False
            else:
                print("Please enter either 1 or 2.")

    def play(self):
        print("Welcome to Tic Tac Toe!")
        print("You're 'X'. The AI is 'O'.")
        input("Press Enter to start playing...")

        while True:
            self.reset_game()
            game_over = False

            while not game_over:
                self.draw_board()

                if self.current_player == "User":
                    move = self.get_user_input()
                    if move is None or not self.mark_board(move, 'X'):
                        print("Invalid move. Try again.")
                        continue
                else:
                    print("AI is thinking...")
                    ai_move = self.get_ai_move()
                    self.mark_board(ai_move, 'O')

                if self.check_winner():
                    self.display_winner()
                    game_over = True
                elif self.is_draw():
                    self.display_winner()
                    game_over = True
                else:
                    self.switch_player()

            if not self.ask_to_play_again():
                print("Thanks for playing!")
                break

# Run the game
if __name__ == "__main__":
    plt.ion()
    game = TicTacToe()
    game.play()
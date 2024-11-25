import random
import csv
import os


class Field:

    def __init__(self):
        self.plain = [
            ["_", "_", "_"],
            ["_", "_", "_"],
            ["_", "_", "_"],
        ]

    def display_plain(self):
        x, y, z = 1, 2, 3
        rows = len(self.plain)
        for r in range(rows):
            print(self.plain[r][0], "|", self.plain[r][1], "|", self.plain[r][2], f"   {x}|{y}|{z}   ")
            x += 3
            y += 3
            z += 3

    def check_coordinate(self, position, symbol):
        row, col = divmod(int(position) - 1, 3)
        if self.plain[row][col] == "_":
            self.plain[row][col] = symbol
            return True
        return False

    def get_flat_board(self):
        return [cell for row in self.plain for cell in row]


class Player:

    def __init__(self, nickname, is_npc=False):
        self.is_npc = is_npc
        self.nickname = nickname
        self.action = None

    def npc_make_action(self, field):
        board = field.get_flat_board()
        opponent_action = 'O' if self.action == 'X' else 'X'

        for combo in Game.WINNING_COMBOS:
            positions = [board[i] for i in combo]
            if positions.count('_') == 1:
                empty_index = positions.index('_')
                move = combo[empty_index] + 1

                if positions.count(self.action) == 2:
                    return str(move)

                if positions.count(opponent_action) == 2:
                    return str(move)

        if board[4] == '_':
            return '5'

        for i in [0, 2, 6, 8]:
            if board[i] == '_':
                return str(i + 1)

        available_moves = [i + 1 for i, cell in enumerate(board) if cell == '_']
        return str(random.choice(available_moves))

    @staticmethod
    def npc_random_action(field):
        board = field.get_flat_board()
        available_moves = [i + 1 for i, cell in enumerate(board) if cell == '_']
        return str(random.choice(available_moves))

    def choose_action(self, field):
        if random.random() < 0.5:
            return self.npc_make_action(field)
        else:
            return self.npc_random_action(field)

    @staticmethod
    def who_goes_first(player_1, player_2):
        first = random.choice([player_1, player_2])
        print(f"{first.nickname} goes first!")
        return first


class Game:
    WINNING_COMBOS = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6],  # Diagonal
    )

    def __init__(self, player: Player, npc: Player):
        self.player = player
        self.npc = npc
        self.player_wins = 0
        self.npc_wins = 0
        self.tie = 0
        self.intro()
        self.last_match_number = None

        file_name = "record.csv"
        if not os.path.exists(file_name):
            with open(file_name, "w", newline="\n") as f:
                writer = csv.writer(f)
                header = ["Nickname", "Player_Wins", "Tie", "NPC", "NPC_Wins"]
                writer.writerow(header)
        else:
            with open("record.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    last_row = row
                    print(last_row[0])

            self.last_match_number = int(last_row[0])

    def intro(self):
        have_action = False
        while not have_action:
            self.player.action = input(f"{self.player.nickname}, choose X or O: ").upper()
            if self.player.action == "X":
                self.npc.action = "O"
            elif self.player.action == "O":
                self.npc.action = "X"
            else:
                print("Only choose X or O")
                continue

            if self.player.action and self.npc.action:
                print(
                    f"{self.player.nickname} has chosen {self.player.action}, "
                    f"{self.npc.nickname} has chosen {self.npc.action}"
                )
                have_action = True
                first_player = Player.who_goes_first(self.player, self.npc)
                self.round(first_player)
            self.play_again()

    def play_again(self):
        while True:
            restart = input("Do you want to play again? (y/n): ").lower()
            if restart == "y":
                self.intro()
                break
            elif restart == "n":
                self.save_results()
                exit("Thanks for playing!")
            else:
                print("Please enter y or n")

    def check_winner(self, field):
        board = field.get_flat_board()
        for combo in self.WINNING_COMBOS:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != "_":
                return board[combo[0]]
        if "_" not in board:
            return "Draw"
        return None

    def round(self, first_player):
        field = Field()
        current_player = first_player
        while True:
            field.display_plain()

            if current_player == self.player:
                input_ok = False
                while not input_ok:
                    position = input(f"{self.player.nickname}, choose a position 1-9: ")
                    if not position.isnumeric() or int(position) < 1 or int(position) > 9:
                        print("Invalid position")
                        continue

                    if field.check_coordinate(position, self.player.action):
                        input_ok = True
                        winner = self.check_winner(field)
                        if winner:
                            field.display_plain()
                            if winner == "Draw":
                                print("It's a tie!")
                                self.tie += 1
                            else:
                                print(f"{self.player.nickname} wins!")
                                self.player_wins += 1
                            return True
                    else:
                        print("Position already taken! Try again.")
                current_player = self.npc


            elif current_player == self.npc:
                npc_position = self.npc.choose_action(field)
                print(f"{self.npc.nickname} chooses position {npc_position}")
                if field.check_coordinate(npc_position, self.npc.action):
                    winner = self.check_winner(field)
                    if winner:
                        field.display_plain()
                        if winner == "Draw":
                            print("It's a tie!")
                            self.tie += 1
                        else:
                            print(f"{self.npc.nickname} wins!")
                            self.npc_wins += 1
                        return True
                current_player = self.player

    def save_results(self):
        with open("record.csv", mode="a", newline="") as f:
            writer = csv.writer(f)
            records = [self.last_match_number, self.player.nickname, self.player_wins, self.tie, self.npc_wins]
            writer.writerow(
                [self.player.nickname,
                 self.player_wins,
                 self.tie,
                 self.npc.nickname,
                 self.npc_wins],

            )
            writer.writerow(records)
            print(
                f"Results saved: {self.player.nickname} {self.player_wins}"
                f" {self.tie} {self.npc.nickname} {self.npc_wins}"
            )


print("Welcome to Tic Tac Toe!")
player_1 = Player(nickname=input("Enter your nickname: "))
player_2 = Player(nickname="NPC", is_npc=True)

Game(player_1, player_2)

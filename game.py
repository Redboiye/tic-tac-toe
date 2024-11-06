import random
import csv


class Field:

    def __init__(self):

        self.plain = [
            ["_", "_", "_"],
            ["_", "_", "_"],
            ["_", "_", "_"],
        ]
        self.plain_coordinates = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
        ]

    def display_plain(self):
        x, y, z = 1, 2, 3

        rows = len(self.plain)
        for r in range(rows):
            # print(self.plain_coordinates[r][0], "|", self.plain_coordinates[r][1], "|", self.plain_coordinates[r][2])
            print(self.plain[r][0], "|", self.plain[r][1], "|", self.plain[r][2], f"   {x}|{y}|{z}   ")
            x += 3
            y += 3
            z += 3

    # logika kas nosaka speletaja, simbola poziciju un plaina
    def check_coordinate(self, position, symbol):
        row, col = divmod(int(position) - 1, 3)
        if self.plain[row][col] == "_":
            self.plain[row][col] = symbol
            return True
        return False


class Player:

    def __init__(self, nickname, is_npc=False):
        self.is_npc = is_npc
        self.nickname = nickname
        self.action = None

    @staticmethod
    def npc_make_action():
        return random.choice(range(1, 9))


class Game:
    WINNING_COMBOS = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Hor
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Ver
        [0, 4, 8], [2, 4, 6],  # Dia
    )

    def __init__(self, player: Player, npc: Player):
        self.player = player
        self.npc = npc
        self.player_wins = 0
        self.npc_wins = 0
        self.intro()

    def intro(self):
        have_action = False
        while not have_action:
            self.player.action = input(f"{self.player.nickname}, choose X or O: ")
            if self.player.action == "X":
                self.npc.action = "O"
            elif self.player.action == "O":
                self.npc.action = "X"
            else:
                print("only choose X or O")
                continue

            if self.player.action and self.npc.action:
                print(
                    f"{self.player.nickname} has chosen"
                    f" {self.player.action},"
                    f" {self.npc.nickname} has chosen {self.npc.action}"
                )
                have_action = True
                round_finished = self.round()
                if round_finished:
                    have_action = False
            self.play_again()

    def play_again(self):
        while True:
            restart = input("Do you want to play again? (y/n): ")
            if restart == "y":
                self.intro()
                break
            elif restart == "n":
                self.save_results()
                exit("Thanks for playing!")
            else:
                print("Please enter y or n")

    def check_winner(self, field):
        board = [cell for row in field.plain for cell in row]
        for combo in self.WINNING_COMBOS:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != "_":
                return board[combo[0]]
        if "_" not in board:
            return "Draw"
        return None

    def round(self, ):
        field = Field()
        while True:
            input_ok = False
            while not input_ok:
                field.display_plain()
                position = input(f"{self.player.nickname} choose a position 1-9: ")
                if not position.isnumeric() or int(position) < 1 or int(position) > 9:
                    print("invalid position")
                    continue

                if field.check_coordinate(position, self.player.action):
                    input_ok = True
                    winner = self.check_winner(field)
                    if winner:
                        field.display_plain()
                        if winner == "Draw":
                            print("it's a tie!")
                        else:
                            print(f"{self.player.nickname} wins!")
                            self.player_wins += 1
                        return True

                else:
                    print("Invalid! Try again.")

                npc_input_ok = False
                while not npc_input_ok:
                    npc_position = self.npc.npc_make_action()
                    if field.check_coordinate(npc_position, self.npc.action):
                        npc_input_ok = True
                        winner = self.check_winner(field)
                        if winner:
                            field.display_plain()
                            if winner == "Draw":
                                print("it's a tie!")
                            else:
                                print(f"{self.npc.nickname} wins!")
                                self.npc_wins += 1
                                return True

    def save_results(self):
        with open("record.csv", mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.player.nickname, self.player_wins, " - ", self.npc.nickname, self.npc_wins])
            print(f"Results saved: {self.player.nickname} {self.player_wins} - {self.npc.nickname} {self.npc_wins}")


print("Welcome to tic tac toe!")
player_1 = Player(nickname=input("Enter your nickname: "))
player_2 = Player(nickname="npc", is_npc=True)

Game(player_1, player_2)

# flagi = ir boolean vertibas(true or false) kuri mainigies sakas ar on off etc., to varam kontroloet while loops(while loop strada pec trigera)

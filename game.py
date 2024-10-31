import random


class Field:
    plain = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"],
    ]


class Player:
    action: str

    def __init__(self, nickname, is_npc=False):
        self.is_npc = is_npc
        self.nickname = nickname

    def get_random_action(self):
        pass


class Game:

    def __init__(self, player: Player, npc: Player):
        self.field = Field()
        self.player = player
        self.npc = npc
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
                self.round()

            else:
                print("Invalid! Try again.")

    def round(self):
        have_winner = False
        print(self.field.plain)
        while not have_winner:
            pass


print("Welcome to tic tac toe!")
player_1 = Player(nickname=input("Enter your nickname: "))
player_2 = Player(nickname="npc", is_npc=True)

Game(player_1, player_2)

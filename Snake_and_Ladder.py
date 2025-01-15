from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import random

# --- Models ---


class Player:
    def __init__(self, name: str):
        self.name = name
        self.position = 0

    def move(self, steps: int):
        self.position += steps

    def set_position(self, position: int):
        self.position = position


# --- Interfaces (SOLID: Interface Segregation Principle) ---
class BoardEntity(ABC):
    @abstractmethod
    def apply(self, position: int) -> int:
        pass


# --- Concrete Implementations ---
class Snake(BoardEntity):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def apply(self, position: int) -> int:
        return self.end if position == self.start else position


class Ladder(BoardEntity):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def apply(self, position: int) -> int:
        return self.end if position == self.start else position


class Dice:
    def __init__(self, sides: int = 6):
        self.sides = sides

    def roll(self) -> int:
        return random.randint(1, self.sides)


# --- Board Class ---
class Board:
    def __init__(self, size: int, entities: List[BoardEntity]):
        self.size = size
        self.entities = entities

    def get_final_position(self, position: int) -> int:
        for entity in self.entities:
            position = entity.apply(position)
        return position


# --- Game Class ---
class SnakeAndLadderGame:
    def __init__(self, board: Board, players: List[Player], dice: Dice):
        self.board = board
        self.players = players
        self.dice = dice
        self.winner: Optional[Player] = None

    def play_turn(self, player: Player):
        roll = self.dice.roll()
        print(f"{player.name} rolled a {roll}")

        new_position = player.position + roll

        if new_position > self.board.size:
            print(f"{player.name} stays at position {player.position}")
            return

        new_position = self.board.get_final_position(new_position)
        print(f"{player.name} moves to position {new_position}")
        player.set_position(new_position)

        if new_position == self.board.size:
            self.winner = player

    def play(self):
        print("Starting Snake and Ladder Game!")
        while not self.winner:
            for player in self.players:
                self.play_turn(player)
                if self.winner:
                    print(f"{self.winner.name} wins the game!")
                    return


def main():
    # Initialize players
    players = [Player("Alice"), Player("Bob")]

    # Initialize snakes and ladders
    snakes = [Snake(14, 7), Snake(31, 26), Snake(78, 35)]
    ladders = [Ladder(3, 22), Ladder(8, 30), Ladder(28, 84)]

    # Initialize board
    board_size = 100
    board_entities = snakes + ladders
    board = Board(board_size, board_entities)

    # Initialize dice
    dice = Dice()

    # Start the game
    game = SnakeAndLadderGame(board, players, dice)
    game.play()


# --- Main Function ---
if __name__ == "__main__":
    main()

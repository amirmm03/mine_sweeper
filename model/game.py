import random


class Game:

    def __init__(self, tool, arz, bomb_number, difficulty):
        self.bomb_number = bomb_number
        self.arz = arz
        self.tool = tool
        self.board: list[list[Button]] = []
        self.start_board()
        self.lost = False
        self.difficulty = difficulty

    def start_board(self):

        for i in range(self.arz):
            row = []
            for j in range(self.tool):
                row.append(Button(False, False, False))

            self.board.append(row)

        for i in range(self.bomb_number):
            self.add_bomb()

        for i in range(self.arz):
            for j in range(self.tool):
                self.find_bombs(i, j)

    def find_bombs(self, i, j):
        ans = 0
        diffs = (-1, 0, 1)
        for idiff in diffs:
            for jdiff in diffs:
                if self.has_bomb(i + idiff, j + jdiff):
                    ans += 1
        self.board[i][j].neighbor_bombs = ans

    def add_bomb(self):
        while True:

            arz = random.randint(0, self.arz - 1)
            tool = random.randint(0, self.tool - 1)
            if not self.board[arz][tool].has_bomb:
                self.board[arz][tool].has_bomb = True
                break

    def has_bomb(self, i, j):
        if i < 0 or j < 0 or i >= self.arz or j >= self.tool:
            return False
        return self.board[i][j].has_bomb


class Button:
    def __init__(self, is_opened, has_flag, has_bomb):
        self.has_bomb = has_bomb
        self.has_flag = has_flag
        self.is_opened = is_opened
        self.neighbor_bombs = 0


now_game: Game

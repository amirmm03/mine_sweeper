from model import game
from model.users import GameHistory, User
from view.menu import ChooseGameMenu, GameMenu


class FirstMenuController:

    def show_history(self):
        GameHistory.show()

    def save(self):
        GameHistory.save()

    def play(self):
        menu = ChooseGameMenu(ChooseGameController())
        menu.run()


class ChooseGameController:
    EASY = (5, 5, 3)
    MEDIUM = (10, 10, 12)
    HARD = (20, 10, 24)

    def play_easy(self):
        self._start_game(self.EASY, "easy")

    def play_medium(self):
        self._start_game(self.MEDIUM, "medium")

    def play_hard(self):
        self._start_game(self.HARD, "hard")

    def play_custom(self, tool, arz, bomb_num):
        self._start_game((tool, arz, bomb_num), "custom")

    def _start_game(self, args, difficulty):
        game.now_game = game.Game(*args, difficulty)
        menu = GameMenu(GameController())
        menu.run()


class GameController:
    def print_board(self):
        board = game.now_game.board
        for row in board:
            for cell in row:
                if cell.is_opened:
                    print(cell.neighbor_bombs, end=" ")
                else:
                    if cell.has_flag:
                        print("F", end=" ")
                    else:
                        print("?", end=" ")

            print()

    def lost(self):
        if game.now_game.lost:
            User.current_user.score = -1
            new_his = GameHistory(User.current_user, False, game.now_game.difficulty)
            GameHistory.all_history.append(new_his)
            return True
        return False

    def won(self):
        number_of_unopened = 0
        for row in game.now_game.board:
            for cell in row:
                if not cell.is_opened:
                    number_of_unopened += 1

        if number_of_unopened == game.now_game.bomb_number:
            User.current_user.score = game.now_game.tool * game.now_game.arz * game.now_game.bomb_number
            new_his = GameHistory(User.current_user, True, game.now_game.difficulty)
            GameHistory.all_history.append(new_his)
            return True
        return False

    def flag(self, tool, arz):
        cell = game.now_game.board[arz][tool]
        cell.has_flag = True

    def unflag(self, tool, arz):
        cell = game.now_game.board[arz][tool]
        cell.has_flag = False

    def open(self, tool, arz):
        if arz < 0 or tool < 0 or arz >= game.now_game.arz or tool >= game.now_game.tool:
            return
        cell = game.now_game.board[arz][tool]
        if cell.has_bomb:
            game.now_game.lost = True
            return

        self.recursive_open(tool, arz)

    def recursive_open(self, tool, arz):
        if arz < 0 or tool < 0 or arz >= game.now_game.arz or tool >= game.now_game.tool:
            return

        cell = game.now_game.board[arz][tool]
        if cell.is_opened:
            return

        cell.is_opened = True
        if cell.neighbor_bombs == 0:
            diffs = (-1, 0, 1)
            for tooldiff in diffs:
                for arzdiff in diffs:
                    if not (tooldiff == 0 and arzdiff == 0):
                        self.recursive_open(tool + tooldiff, arz + arzdiff)

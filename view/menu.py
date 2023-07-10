from model.users import User


class Menu:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        pass


class FirstMenu(Menu):
    def __init__(self, controller):
        super().__init__(controller)

    def run(self):
        while True:
            cmd = input("enter command (play history exit) ")

            if cmd == "exit":
                self.controller.save()
                return
            elif cmd == "play":
                print("entering game select menu")
                self.controller.play()
            elif cmd == "history":
                self.controller.show_history()
            else:
                print("invalid command")


class ChooseGameMenu(Menu):
    def __init__(self, controller):
        super().__init__(controller)

    def run(self):

        name = input("enter your name: ")
        User.current_user = User(name)

        options = ["easy", "medium", "hard", "costume"]
        while True:
            cmd = input("enter command (" + options[0] + " " + options[1] + " " + options[2] + " " + options[3] + ")")

            if cmd == options[0]:
                print("game started")
                self.controller.play_easy()
                return
            elif cmd == options[1]:
                print("game started")
                self.controller.play_medium()
                return
            elif cmd == options[2]:
                print("game started")
                self.controller.play_hard()
                return
            elif cmd.startswith(options[3]):
                tool, arz, b_num = 0, 0, 0
                ok = True
                cmd = cmd.split(" ")

                try:
                    tool, arz, b_num = int(cmd[1]), int(cmd[2]), int(cmd[3])
                except Exception:
                    ok = False
                    print("wrong format")

                if ok:
                    print("game started")
                    self.controller.play_custom(tool, arz, b_num)
                    return
            else:
                print("invalid command")


class GameMenu(Menu):
    def __init__(self, controller):
        super().__init__(controller)

    def run(self):
        options = ["open", "flag", "unflag"]
        self.controller.print_board()
        while True:
            cmd = input("enter command (" + options[0] + " " + options[1] + " " + options[2] + ")")

            if cmd.startswith(options[0]):

                cmd = cmd.split(" ")
                try:
                    tool, arz = int(cmd[1]), int(cmd[2])
                    self.controller.open(tool, arz)
                except Exception:
                    print("wrong format")

            elif cmd.startswith(options[1]):

                cmd = cmd.split(" ")
                try:
                    tool, arz = int(cmd[1]), int(cmd[2])
                    self.controller.flag(tool, arz)
                except Exception:
                    print("wrong format")

            elif cmd.startswith(options[2]):

                cmd = cmd.split(" ")
                try:
                    tool, arz = int(cmd[1]), int(cmd[2])
                    self.controller.unflag(tool, arz)
                except Exception:
                    print("wrong format")

            else:
                print("invalid command")

            if self.controller.lost():
                print("you lost")
                return

            if self.controller.won():
                print("you won")
                return

            self.controller.print_board()

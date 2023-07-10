import pickle


class User:
    current_user = None

    def __init__(self, name):
        self.name = name
        self.score = 0


class GameHistory:
    all_history = None

    def __init__(self, user, has_won, difficulty):
        self.difficulty = difficulty
        self.has_won = has_won
        self.user = user

    @classmethod
    def show(cls):
        if GameHistory.all_history is None:
            GameHistory.load()
        for his in cls.all_history:
            if his:
                print("name:", his.user.name, "score:", his.user.score,
                      "difficulty:", his.difficulty, "won:", his.has_won)

    @classmethod
    def save(cls):
        with open("./history", "wb") as f:  # "wb" because we want to write in binary mode
            pickle.dump(cls.all_history, f)

    @classmethod
    def load(cls):
        with open("history", "rb") as f:  # "rb" because we want to read in binary mode
            cls.all_history = pickle.load(f)

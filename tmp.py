import pickle

l = []

with open("history", "wb") as f:  # "wb" because we want to write in binary mode

    pickle.dump(l, f)

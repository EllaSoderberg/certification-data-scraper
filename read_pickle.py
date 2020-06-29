import pickle

def read_pickle(file_name):
    load_pickle = open(file_name, 'rb')
    open_pickle = pickle.load(load_pickle)
    return open_pickle


def save_pickle(to_save, file_name):
    pickle_file = open(file_name, 'wb')
    pickle.dump(to_save, pickle_file)


save_pickle(["eh", "oh", "uo"], "evergabe.pickle")

print(read_pickle("evergabe.pickle"))
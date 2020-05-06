import pickle


def save_csv(link_list, file_name):
    # Takes a list and saves it as a csv
    file = open(file_name, 'w', encoding="utf8")
    for link in link_list:
        file.write(str(link) + "\n")
    file.close


def read_csv(file_name):
    # Reads a csv, saves each line to a list and returns the list
    linkfile = open(file_name, 'r', encoding="utf8")
    link_list = []
    for link in linkfile.readlines():
        link_list.append(link.strip())
    return link_list


def save_pickle(to_save, file_name):
    pickle_file = open(file_name, 'wb')
    pickle.dump(to_save, pickle_file)


def read_pickle(file_name):
    load_pickle = open(file_name, 'rb')
    open_pickle = pickle.load(load_pickle)
    return open_pickle

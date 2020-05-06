contact_list = []
file = open("TED_contacts.csv", "r")
for row in file.readlines():
    contact_list.append(row)
print(len(contact_list))
unique = list(set(contact_list))
print(unique)
print(len(unique))
new_file = open("TED_contacts.csv", "w")

for row in unique:
    new_file.write(row)

"""
import pickle


def save_pickle(to_save, file_name):
    pickle_file = open(file_name, 'wb')
    pickle.dump(to_save, pickle_file)


contact_list = []
contacts2 = []
file = open("TED_contacts.csv", "r")
for row in file.readlines():
    contact_list.append(row.strip())

save_pickle(contact_list, "TED_contacts.p")
"""
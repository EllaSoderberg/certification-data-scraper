"""
from FileHandleler import HandleFiles
import time
handler = HandleFiles("hej", "hoj")
handler.extract_files(["zip"])
time.sleep(60)
handler.read_pdfs()
print(handler.folder_list)
time.sleep(20)
handler.read_docx()
print(handler.folder_list)
time.sleep(20)
"""

#handler.delete_all_files()
new_contact = []

def find_duplicates(new_contact):
    with open("contacts.csv") as file:
        contact_list = file.read().split("\\n")
    for contact in contact_list:
        print(contact)
        if new_contact[3:-3] in contact:
            return True
        else:
            new_contact.append(new_contact)
            return False


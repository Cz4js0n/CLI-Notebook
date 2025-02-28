import json
import hashlib
from cryptography.fernet import Fernet


#Function that check if password is correct
def authorization(password):
    #Hashing password with sha256 standard
    hashed_password = hashlib.sha256(password).hexdigest()
    with open("data.json", "r") as file:
        data = json.load(file)
        if hashed_password == data["Password"]:
            return True
        else:
            return False


#Function that generates key
def get_key():
    try:
        with open("key.txt", "rb") as file:
            return file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("key.txt", "wb") as file:
            file.write(key)
        return key


#Function that creates note coded with sha256 standard
def create_note():
    #Generate key and cipher for key
    key = get_key()
    cipher = Fernet(key)
    name = input("Enter note name: ")
    #Encrypt name of a note
    hashed_name = cipher.encrypt(name.encode()).decode()
    content = input("Enter note content: ")
    #Encrypt content of a note
    hashed_content = cipher.encrypt(content.encode()).decode()
    try:
        with open("notes.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []


    data.append({"Name": hashed_name, "Content": hashed_content})

    with open("notes.json", "w") as file:
        json.dump(data, file, indent=4)


#Function that display note
def display_note():
    #Get a key and cipher for key
    key = get_key()
    cipher = Fernet(key)
    #Load notes
    with open("notes.json", "r") as file:
        data = json.load(file)
    #In this loop print all names of notes
    for note in data:
        print(cipher.decrypt(note["Name"]).decode())
    name = input("Which note do you want to display: ")
    #In this loop print content for chosen note
    for note in data:
        if cipher.decrypt(note["Name"]).decode() == name:
            print(cipher.decrypt(note["Content"]).decode())


#Function that delete chosen note
def delete_note():
    key = get_key()
    cipher = Fernet(key)
    with open("notes.json", "r") as file:
        data = json.load(file)
    for note in data:
        print(cipher.decrypt(note["Name"]).decode())
    name = input("Which note do you want to delete: ")
    new_data = []
    for note in data:
        if cipher.decrypt(note["Name"]).decode() != name:
            new_data.append(note)
    with open("notes.json", "w") as file:
        json.dump(new_data, file, indent=4)


#Function that edit content of chosen note
def edit_note():
    key = get_key()
    cipher = Fernet(key)
    with open("notes.json", "r") as file:
        data = json.load(file)
    #In this loop print all names of notes
    for note in data:
        print(cipher.decrypt(note["Name"]).decode())
    name = input("Which note do you want to edit: ")
    #In this loop print content for chosen note
    for note in data:
        if cipher.decrypt(note["Name"]).decode() == name:
            print(f"Content of a current note: {cipher.decrypt(note["Content"]).decode()}")
    new_content = input("New content of the note: ")
    for note in data:
        if cipher.decrypt(note["Name"]).decode() == name:
            note["Content"] = cipher.encrypt(new_content.encode()).decode()
    with open("notes.json", "w") as file:
        json.dump(data, file, indent=4)


#Main function
def main():
    #User data
    password = input("Password: ")


    #Check authorization
    if authorization(password.encode("utf-8")):
        print("Authenticated")
        operation = input("Which operation do you want to perform (Create/Display/Delete/Edit): ")
        if operation.lower() == "create":
            create_note()
        elif operation.lower() == "display":
            display_note()
        elif operation.lower() == "delete":
            delete_note()
        elif operation.lower() == "edit":
            edit_note()
    else:
        print("Not Authenticated")


if __name__ == "__main__":
    main()
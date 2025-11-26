import bcrypt
import os
USER_DATA_FILE = "users.txt"



#HASHING THE PASSWORD
def hash_password(plain_text_password):
    pw_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed.decode("utf-8")

new_function = 1

#VERIFY PASSWORD
def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(
        plain_text_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


#CHECK IF USERNAME EXISTS
def user_exists(username):
    # If the file does not exist yet, no users exist
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username = line.strip().split(",")[0]
            if stored_username == username:
                return True
    return False

#REGISTERING A NEW USER
def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed = hash_password(password)

    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed}\n")

    print(f"user '{username}' registered successfully!")
    return True

#LOGING IN A USER
def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("Error:no user is registered yet.")
        return False

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username, stored_hash = line.strip().split(",")

            if stored_username == username:
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    print("Error: Username not found.")
    return False

#VALIDATION FUNCTION
def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if not username.isalnum():
        return False, "Username must be letters/numbers only."
    return True, ""


def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    return True, ""


#CREATING AN INTERACTIVE MENU THAT WAS GIVEN
def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)


def main():
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            valid, msg = validate_username(username)
            if not valid:
                print("Error:", msg)
                continue

            password = input("Enter a password: ").strip()
            valid, msg = validate_password(password)
            if not valid:
                print("Error:", msg)
                continue

            confirm = input("Confirm password: ").strip()
            if password != confirm:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            login_user(username, password)
            input("\nPress Enter to go back to menu...")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

"""
User Profile Management:
A local JSON database for managing user accounts.
"""

import json
import os
import uuid
from typing import Any

DB_FILE = "users.json"


class UserProfileManager:

    @classmethod
    def load_users(cls) -> list[dict[str, Any]]:
        """Safely loads users, initializing the JSON file if missing or empty."""
        if not os.path.exists(DB_FILE):
            cls.save_users([])
            return []

        try:
            with open(DB_FILE, "r") as file:
                content = file.read().strip()
                if not content:  # If the file is 0 bytes / empty
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            print("\n-------------------------")
            print("Warning: users.json was corrupted. Resetting database.")
            print("-------------------------\n")
            cls.save_users([])
            return []

    @classmethod
    def save_users(cls, users: list[dict[str, Any]]) -> None:
        """Saves user list to JSON database."""
        try:
            with open(DB_FILE, "w") as file:
                json.dump(users, file, indent=4)
        except Exception as e:
            print(f"Error saving to database: {e}")

    @classmethod
    def create_profile(cls, user_data: dict[str, Any]) -> None:
        users = cls.load_users()

        # Check for duplicates before adding
        for user in users:
            if user["Email"].lower() == user_data["Email"].lower():
                print("\n-------------------------")
                print("User with this email already exists.")
                print("-------------------------\n")
                return

        # Assign UUID
        user_data["user_id"] = str(uuid.uuid4())[:8]

        users.append(user_data)
        cls.save_users(users)
        print("\n-------------------------")
        print(f"Profile created successfully! Assigned ID: {user_data['user_id']}")
        print("-------------------------\n")

    @classmethod
    def read_user_profile(cls, email: str) -> None:
        users = cls.load_users()
        for user in users:
            if user["Email"].lower() == email.lower():
                print("\n--- User Profile Found ---")
                for key, value in user.items():
                    print(f"{key} : {value}")
                print("-------------------------\n")
                return

        print("\n-------------------------")
        print("No user found with that email address.")
        print("-------------------------\n")

    @classmethod
    def update_user_profile(cls, target_email: str, updated_data: dict[str, Any]) -> None:
        users = cls.load_users()
        for user in users:
            if user["Email"].lower() == target_email.lower():
                user.update(updated_data)
                cls.save_users(users)
                print("\n-------------------------")
                print("Profile updated successfully!")
                print("-------------------------\n")
                cls.read_user_profile(user["Email"])
                return

        print("\n-------------------------")
        print("Profile not found.")
        print("-------------------------\n")

    @classmethod
    def delete_user_profile(cls, email: str) -> None:
        users = cls.load_users()
        updated_users = [u for u in users if u["Email"].lower() != email.lower()]

        if len(users) == len(updated_users):
            print("\n-------------------------")
            print("User email not found.")
            print("-------------------------\n")
        else:
            cls.save_users(updated_users)
            print("\n-------------------------")
            print("User profile deleted successfully!")
            print("-------------------------\n")


# Main Application Execution Loop
while True:
    try:
        choice = int(
            input(
                "Press:\n1. Create User Profile\n2. Read/Get User Info\n3. Update User Profile\n4. Delete User Profile\n5. Exit\nChoice: "
            )
        )

        if choice < 1 or choice > 5:
            raise ValueError("Choice must be between 1 and 5.")

    except ValueError as e:
        print("\n---------------------------------------------------------------")
        print(f"Invalid Input: {e}")
        print("---------------------------------------------------------------\n")
        continue

    match choice:
        case 1:
            try:
                name = input("Enter your name:\n")
                age = int(input("Enter your age:\n"))
                if age <= 0 or age > 100:
                    raise ValueError("Please enter a valid age (1-100).")

                ph_no = int(input("Enter your phone number:\n"))
                address = input("Enter your address:\n")
                email = input("Enter your email:\n")

                user_data = {
                    "Name": name,
                    "Age": age,
                    "Phone number": ph_no,
                    "Address": address,
                    "Email": email,
                }
                UserProfileManager.create_profile(user_data)
            except ValueError as e:
                print(f"\n[!] Input Error: {e}\n")

        case 2:
            email = input("Enter your email to view profile:\n")
            UserProfileManager.read_user_profile(email)

        case 3:
            target_email = input("Enter your email to locate profile:\n")
            users = UserProfileManager.load_users()

            if any(u["Email"].lower() == target_email.lower() for u in users):
                try:
                    # FIX 1: Wrap string in input()
                    to_update = input("What do you want to update? (Name, Age, Phone number, Address, Email): ").strip().lower()

                    match to_update:
                        case "name":
                            name = input("Enter new name:\n")
                            UserProfileManager.update_user_profile(target_email, {"Name": name})

                        case "age":
                            age = int(input("Enter new age:\n"))
                            if age < 1 or age > 100:
                                raise ValueError("Please enter a valid age (1-100).")
                            UserProfileManager.update_user_profile(target_email, {"Age": age})

                        case "phone number" | "phone":
                            ph_no = int(input("Enter new phone number:\n"))
                            UserProfileManager.update_user_profile(target_email, {"Phone number": ph_no})

                        case "address":
                            address = input("Enter new address:\n")
                            UserProfileManager.update_user_profile(target_email, {"Address": address})

                        case "email":
                            new_email = input("Enter new email:\n")
                            UserProfileManager.update_user_profile(target_email, {"Email": new_email})

                        case _:
                            print("\n[!] Invalid field choice.\n")

                except ValueError as e:
                    print(f"\n[!] Input Error: {e}\n")
            else:
                print("\n[!] Profile not found.\n")

        case 4:
            email = input("Enter email to delete profile:\n")
            UserProfileManager.delete_user_profile(email)

        case 5:
            print("Thank you! Please visit again.")
            break
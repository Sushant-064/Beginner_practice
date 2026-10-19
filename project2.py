import json
import os
import uuid
from datetime import datetime
from typing import Any

DB_FILE = "expenses.json"


# Matching the prompt's requested custom exception name
class InvalidAmountError(Exception):
    pass


class ExpenseTracker:

    @classmethod
    def load_expenses(cls) -> list[dict[str, Any]]:
        if not os.path.exists(DB_FILE):
            cls.save_expenses([])
            return []

        try:
            with open(DB_FILE, "r") as file:
                content = json.load(file)
                return content if content else []
        except json.JSONDecodeError:
            print(
                "\n---------------------------------------------------------------"
            )
            print("Warning: Database was corrupted. Resetting data.")
            print(
                "---------------------------------------------------------------\n"
            )
            cls.save_expenses([])
            return []

    @classmethod
    def save_expenses(cls, expenses: list[dict[str, Any]]) -> None:
        try:
            with open(DB_FILE, "w") as file:
                json.dump(expenses, file, indent=4)
        except Exception as e:
            print(f"Error saving to database: {e}")

    @classmethod
    def create_expense(cls, expense_data: dict[str, Any]) -> None:
        expenses = cls.load_expenses()
        expense_data["id"] = str(uuid.uuid4())[:5]
        expense_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        expenses.append(expense_data)
        cls.save_expenses(expenses)
        print("\n-------------------------------------------")
        print("Expense successfully saved!")
        print(f"Assigned ID: {expense_data['id']}")
        print("-------------------------------------------\n")

    @classmethod
    def delete_expense(cls, expense_id: str) -> None:
        expenses = cls.load_expenses()
        new_expenses = [
            e for e in expenses if e["id"].lower() != expense_id.lower()
        ]

        if len(expenses) == len(new_expenses):
            print("\n[!] Expense ID not found.\n")
        else:
            cls.save_expenses(new_expenses)
            print("\n----------------------------------")
            print("Expense deleted successfully.")
            print("----------------------------------\n")

    @classmethod
    def calc_total_expenses(cls) -> None:
        expenses = cls.load_expenses()
        total = sum(expense["Amount"] for expense in expenses)
        print("\n-------------------------------------------")
        print(f"Total spending across all expenses: ${total:.2f}")
        print("-------------------------------------------\n")

    @classmethod
    def read_expenses(cls) -> None:
        expenses = cls.load_expenses()
        if not expenses:
            print("\n[!] No expenses stored yet.\n")
            return

        print("\n--- All Recorded Expenses ---")
        for item in expenses:
            print(
                f"ID: {item['id']} | Item: {item['Item name']} | Category: {item['Category']} | Amount: ${item['Amount']} | Date: {item['Date']}"
            )
        print("-----------------------------\n")

    @classmethod
    def update_expense(
        cls, expense_id: str, data_to_update: dict[str, Any]
    ) -> None:
        expenses = cls.load_expenses()
        for expense in expenses:
            if expense["id"].lower() == expense_id.lower():
                expense.update(data_to_update)
                cls.save_expenses(expenses)
                print("\n----------------------------------")
                print("Expense updated successfully!")
                print("----------------------------------\n")
                return

        print("\n[!] Expense ID not found.\n")


# Main Application Loop
while True:
    print("Press:")
    print("1. Add new expense")
    print("2. Read all expenses")
    print("3. Calculate total spending")
    print("4. Update expense")
    print("5. Delete expense")
    print("6. Exit")

    try:
        choice = int(input("Choice: "))
        if choice < 1 or choice > 6:
            raise ValueError("Option must be between 1 and 6.")
    except ValueError as e:
        print(f"\n[!] Invalid input choice: {e}\n")
        continue

    match choice:
        case 1:
            try:
                itm_name = input("Enter item name: ")
                category = input("Enter category: ")

                # Catches ValueError if user enters words like "twenty"
                amount_input = float(input("Enter amount: "))
                if amount_input <= 0:
                    raise InvalidAmountError(
                        "Expense amount must be greater than zero."
                    )

                date_str = input(
                    "Enter date (YYYY-MM-DD) [Leave blank for today]: "
                )
                if not date_str.strip():
                    date_str = datetime.now().strftime("%Y-%m-%d")

                expense_payload = {
                    "Item name": itm_name,
                    "Category": category,
                    "Amount": amount_input,
                    "Date": date_str,
                }
                ExpenseTracker.create_expense(expense_payload)

            except ValueError:
                print(
                    "\n[!] Input Error: Amount must be a valid number (e.g. 20.0 or 15).\n"
                )
            except InvalidAmountError as e:
                print(f"\n[!] Custom Exception: {e}\n")

        case 2:
            ExpenseTracker.read_expenses()

        case 3:
            ExpenseTracker.calc_total_expenses()

        case 4:
            target_id = input("Enter expense ID to update: ")
            to_update = (
                input("What to update? (Category, Amount, Date): ")
                .strip()
                .lower()
            )

            try:
                match to_update:
                    case "category":
                        val = input("Enter new category: ")
                        ExpenseTracker.update_expense(
                            target_id, {"Category": val}
                        )

                    case "amount":
                        val = float(input("Enter new amount: "))
                        if val <= 0:
                            raise InvalidAmountError(
                                "Amount must be greater than zero."
                            )
                        ExpenseTracker.update_expense(target_id, {"Amount": val})

                    case "date":
                        val = input("Enter new date (YYYY-MM-DD): ")
                        ExpenseTracker.update_expense(target_id, {"Date": val})

                    case _:
                        print("\n[!] Invalid field choice.\n")

            except ValueError:
                print("\n[!] Input Error: Amount must be a number.\n")
            except InvalidAmountError as e:
                print(f"\n[!] Custom Exception: {e}\n")

        case 5:
            target_id = input("Enter expense ID to delete: ")
            ExpenseTracker.delete_expense(target_id)

        case 6:
            print("Exiting Expense Tracker. Goodbye!")
            break
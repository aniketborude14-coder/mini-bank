import json
import os
import random

DATA_FILE = "accounts.json"


def load_accounts():
    """Load account data from JSON file if it exists."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_accounts(accounts):
    """Save all account data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(accounts, f, indent=4)


def generate_account_number(accounts):
    """Generate a unique 10-digit account number."""
    while True:
        acc_no = str(random.randint(1000000000, 9999999999))
        if acc_no not in accounts:
            return acc_no


def log_transaction(account, description):
    """Append a transaction record to account history."""
    account["transactions"].append(description)


def create_account(accounts):
    print("\n--- Open a New Account ---")
    
    while True:
        name = input("Enter Full Name (First and Last): ").strip()
        if len(name.split()) >= 2:
            break
        print("Error: Please provide at least first and last name.")

    while True:
        pin = input("Set a 4-digit numeric PIN: ").strip()
        if len(pin) == 4 and pin.isdigit():
            break
        print("Error: PIN must be exactly 4 digits.")

    while True:
        try:
            initial_deposit = float(input("Enter initial deposit amount: ₹"))
            if initial_deposit < 0:
                print("Error: Initial deposit cannot be negative.")
                continue
            break
        except ValueError:
            print("Error: Enter a valid numeric amount.")

    acc_no = generate_account_number(accounts)
    accounts[acc_no] = {
        "name": name,
        "pin": pin,
        "balance": initial_deposit,
        "failed_attempts": 0,
        "is_locked": False,
        "transactions": [f"Account opened with deposit: ₹{initial_deposit:.2f}"]
    }
    save_accounts(accounts)

    print(f"\nAccount Created Successfully!")
    print(f"Account Number : {acc_no}")
    print(f"Account Holder : {name}")
    print(f"Current Balance: ₹{initial_deposit:.2f}")


def customer_portal(acc_no, accounts):
    """Authenticated session menu for logged-in user."""
    account = accounts[acc_no]

    while True:
        print(f"\n=== Welcome, {account['name']} ===")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. View Last 5 Transactions")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            print(f"\nCurrent Balance: ₹{account['balance']:.2f}")

        elif choice == "2":
            try:
                amt = float(input("Enter deposit amount: ₹"))
                if amt <= 0:
                    print("Error: Deposit amount must be positive.")
                    continue
                account["balance"] += amt
                log_transaction(account, f"Deposited: +₹{amt:.2f}")
                save_accounts(accounts)
                print(f"Deposited ₹{amt:.2f}. New Balance: ₹{account['balance']:.2f}")
            except ValueError:
                print("Error: Invalid numeric input.")

        elif choice == "3":
            try:
                amt = float(input("Enter withdrawal amount: ₹"))
                if amt <= 0:
                    print("Error: Withdrawal amount must be positive.")
                elif amt > account["balance"]:
                    print(f"Error: Insufficient funds. Available balance: ₹{account['balance']:.2f}")
                else:
                    account["balance"] -= amt
                    log_transaction(account, f"Withdrew: -₹{amt:.2f}")
                    save_accounts(accounts)
                    print(f"Withdrew ₹{amt:.2f}. Remaining Balance: ₹{account['balance']:.2f}")
            except ValueError:
                print("Error: Invalid numeric input.")

        elif choice == "4":
            target_acc = input("Enter recipient's 10-digit Account Number: ").strip()
            if target_acc == acc_no:
                print("Error: You cannot transfer money to your own account.")
                continue
            if target_acc not in accounts:
                print("Error: Destination account does not exist.")
                continue

            try:
                amt = float(input("Enter transfer amount: ₹"))
                if amt <= 0:
                    print("Error: Transfer amount must be positive.")
                elif amt > account["balance"]:
                    print(f"Error: Insufficient funds. Available: ₹{account['balance']:.2f}")
                else:
                    # Deduct from sender
                    account["balance"] -= amt
                    log_transaction(account, f"Transferred to {target_acc}: -₹{amt:.2f}")

                    # Credit to receiver
                    recipient = accounts[target_acc]
                    recipient["balance"] += amt
                    log_transaction(recipient, f"Received from {acc_no}: +₹{amt:.2f}")

                    save_accounts(accounts)
                    print(f"Successfully transferred ₹{amt:.2f} to Account {target_acc}.")
                    print(f"Your Remaining Balance: ₹{account['balance']:.2f}")
            except ValueError:
                print("Error: Invalid numeric input.")

        elif choice == "5":
            print("\n--- Last 5 Transactions ---")
            recent = account["transactions"][-5:]
            if not recent:
                print("No transactions found.")
            else:
                for idx, record in enumerate(reversed(recent), 1):
                    print(f"{idx}. {record}")

        elif choice == "6":
            old_pin = input("Enter current PIN: ").strip()
            if old_pin != account["pin"]:
                print("Error: Current PIN does not match.")
                continue

            new_pin = input("Enter new 4-digit PIN: ").strip()
            if len(new_pin) == 4 and new_pin.isdigit():
                account["pin"] = new_pin
                log_transaction(account, "PIN changed successfully")
                save_accounts(accounts)
                print("PIN updated successfully.")
            else:
                print("Error: New PIN must be exactly 4 digits.")

        elif choice == "7":
            print("Logging out... Thank you for banking with us.")
            break
        else:
            print("Invalid selection. Please choose 1-7.")


def login(accounts):
    print("\n--- Account Login ---")
    acc_no = input("Enter 10-digit Account Number: ").strip()

    if acc_no not in accounts:
        print("Error: Account not found.")
        return

    account = accounts[acc_no]

    if account.get("is_locked", False):
        print("This account is LOCKED due to multiple incorrect attempts. Contact support.")
        return

    entered_pin = input("Enter your 4-digit PIN: ").strip()

    if entered_pin == account["pin"]:
        account["failed_attempts"] = 0
        save_accounts(accounts)
        customer_portal(acc_no, accounts)
    else:
        account["failed_attempts"] = account.get("failed_attempts", 0) + 1
        remaining = 3 - account["failed_attempts"]

        if account["failed_attempts"] >= 3:
            account["is_locked"] = True
            print("Incorrect PIN. Account is now LOCKED due to 3 failed attempts.")
        else:
            print(f"Incorrect PIN. You have {remaining} attempt(s) remaining.")

        save_accounts(accounts)


def main():
    accounts = load_accounts()

    while True:
        print("\n===============================")
        print("      BANKING MANAGEMENT       ")
        print("===============================")
        print("1. Open New Account")
        print("2. Login to Existing Account")
        print("3. Exit System")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            create_account(accounts)
        elif choice == "2":
            login(accounts)
        elif choice == "3":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
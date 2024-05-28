import datetime
import hashlib

class User:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = hashlib.sha256(pin.encode()).hexdigest()
        self.balance = 0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"{datetime.datetime.now()}: Deposit: +{amount}")
        print("\nDeposit successful.")
        print(f"Your new balance is: ${self.balance:.2f}\n")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"{datetime.datetime.now()}: Withdrawal: -{amount}")
            print("\nWithdrawal successful.")
            print(f"Your new balance is: ${self.balance:.2f}\n")
        else:
            print("Insufficient funds!")

    def transfer(self, recipient, amount):
        if self.balance >= amount and recipient:
            self.balance -= amount
            recipient.balance += amount
            self.transactions.append(f"{datetime.datetime.now()}: Transfer to {recipient.user_id}: -{amount}")
            recipient.transactions.append(f"{datetime.datetime.now()}: Transfer from {self.user_id}: +{amount}")
            print("\nTransfer successful.")
            print(f"Your new balance is: ${self.balance:.2f}\n")
        else:
            print("Insufficient funds or invalid recipient!")

    def display_transactions(self):
        print("\nTransaction History:")
        for transaction in self.transactions:
            print(transaction)
        print("\n")

class ATM:
    def __init__(self):
        self.users = {}

    def user_login(self, user_id, pin):
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        if user_id in self.users and hashed_pin == self.users[user_id].pin:
            return self.users[user_id]
        print("Invalid user ID or PIN. Please try again.\n")
        return None

    def add_user(self, user_id, pin):
        if user_id not in self.users:
            user = User(user_id, pin)
            self.users[user_id] = user
            print("User created successfully!")
        else:
            print("User ID already exists! Please choose a different ID.\n")

def main():
    atm = ATM()
    print("Welcome to the ATM System!\n")

    while True:
        print("1. Add User")
        print("2. User Login")
        print("3. Exit")

        main_choice = input("Please select an option (1-3): ")

        if main_choice == "1":
            user_id = input("Enter a user ID: ")
            pin = input("Enter a PIN (4-digits): ")
            atm.add_user(user_id, pin)
            print("\n")

        elif main_choice == "2":
            user_id = input("Enter your user ID: ")
            pin = input("Enter PIN: ")
            current_user = atm.user_login(user_id, pin)
            if current_user:
                while True:
                    print("\n1. Display Transactions History")
                    print("2. Withdraw Money")
                    print("3. Deposit Money")
                    print("4. Transfer Money")
                    print("5. Logout")
                    user_choice = input("What would you like to do? Please choose an option (1-5): ")

                    if user_choice == "1":
                        current_user.display_transactions()
                    elif user_choice == "2":
                        amount = float(input("Enter the amount to withdraw: "))
                        current_user.withdraw(amount)
                    elif user_choice == "3":
                        amount = float(input("Enter the amount to deposit: "))
                        current_user.deposit(amount)
                    elif user_choice == "4":
                        recipient_id = input("Enter recipient's user ID: ")
                        amount = float(input("Enter the amount to transfer: "))
                        recipient = atm.users.get(recipient_id)
                        current_user.transfer(recipient, amount)
                    elif user_choice == "5":
                        print("You have been logged out successfully.\n")
                        break

        elif main_choice == "3":
            print("Thank you for using our ATM System. Goodbye!")
            break

if __name__ == "__main__":
    main()
class Bank:
    def __init__(self):
        self.users = {}
        self.admin_user = {'username': 'aryan', 'password': 'aryan11'}
        self.failed_login_attempts = {}
        self.deposit_limit = 100000
        self.admin_deposit_limit = 300000
        self.withdraw_limit = 50000
        self.conversion_rate = {'INR_to_USD': 0.014}
        self.notifications = []

    def create_account(self, user_id, password):
        if user_id not in self.users:
            self.users[user_id] = {'password': password, 'balance': 50000, 'blocked': False}
            print(f"Account for user {user_id} created successfully. Initial balance: 50,000 INR")
        else:
            print(f"User {user_id} already has an account.")

    def send_money(self, sender_id, recipient_id, amount):
        if sender_id in self.users and recipient_id in self.users:
            if 0 < amount <= self.users[sender_id]['balance']:
                self.users[sender_id]['balance'] -= amount
                self.users[recipient_id]['balance'] += amount
                print(f"Money sent successfully. New balance for {sender_id}: {self.users[sender_id]['balance']} INR")
                print(f"New balance for {recipient_id}: {self.users[recipient_id]['balance']} INR")
            else:
                print("Invalid amount or insufficient funds.")
        else:
            print("Invalid sender or recipient ID.")

    def login(self, user_id, password):
        if user_id in self.users and not self.users[user_id]['blocked']:
            attempts = self.failed_login_attempts.get(user_id, 0)
            if attempts < 3 and self.users[user_id]['password'] == password:
                self.failed_login_attempts[user_id] = 0
                return True
            else:
                print(f"Invalid password. Attempts remaining: {3 - attempts}")
                self.failed_login_attempts[user_id] = attempts + 1
                if attempts + 1 >= 3:
                    print(f"Account for user {user_id} is blocked. Contact the admin to unblock.")
                    self.users[user_id]['blocked'] = True
                    self.failed_login_attempts[user_id] = 0

        return False

    def check_balance(self, user_id):
        return self.users[user_id]['balance']

    def deposit(self, user_id, amount):
        if amount <= self.deposit_limit and (self.users[user_id]['balance'] + amount) <= self.deposit_limit:
            self.users[user_id]['balance'] += amount
            print(f"Deposit successful. New balance: {self.users[user_id]['balance']} INR")
        else:
            print(f"Deposit rejected. Amount exceeds limit of {self.deposit_limit} INR.")

    def withdraw(self, user_id, amount):
        if amount <= self.withdraw_limit and amount <= self.users[user_id]['balance']:
            self.users[user_id]['balance'] -= amount
            print(f"Withdrawal successful. New balance: {self.users[user_id]['balance']} INR")
            self.display_withdrawal_notes(amount)
            if self.users[user_id]['balance'] < 5000:
                self.send_notification_to_admin(user_id)
        else:
            print(f"Withdrawal rejected. Check amount or withdrawal limit of {self.withdraw_limit} INR.")

    def change_password(self, user_id, new_password):
        if user_id in self.users:
            self.users[user_id]['password'] = new_password
            print("Password changed successfully.")
        else:
            print("User not found.")

    def admin_login(self, username, password):
        return username == self.admin_user['username'] and password == self.admin_user['password']

    def block_user(self, admin_id, user_id):
        if admin_id == self.admin_user['username'] and user_id in self.users:
            self.users[user_id]['blocked'] = True
            print(f"User {user_id} blocked by admin.")
        else:
            print("Invalid admin credentials or user not found.")

    def unblock_user(self, admin_id, user_id):
        if admin_id == self.admin_user['username'] and user_id in self.users:
            self.users[user_id]['blocked'] = False
            print(f"User {user_id} unblocked by admin.")
        else:
            print("Invalid admin credentials or user not found.")

    def convert_to_usd(self, user_id):
        inr_balance = self.users[user_id]['balance']
        usd_balance = inr_balance * self.conversion_rate['INR_to_USD']
        print(f"Converted Balance to USD: {usd_balance:.2f}")

    def display_withdrawal_notes(self, amount):
        denominations = [2000, 500, 200, 100]
        notes = {denom: int(amount // denom) for denom in denominations if amount // denom > 0}
        print("Withdrawal Notes:", {denom: count for denom, count in notes.items()})

    def send_notification_to_admin(self, user_id):
        admin_email = 'admin@example.com'  # Replace with actual admin email
        user_balance = self.users[user_id]['balance']
        notification = f"User {user_id} has a low balance of {user_balance}."
        self.notifications.append(notification)
        print(f"Sending notification to admin: {notification}")

    def view_notifications(self):
        print("\nNotifications:")
        for notification in self.notifications:
            print(notification)

    def admin_deposit(self, admin_id, user_id, amount):
        if admin_id == self.admin_user['username'] and user_id in self.users:
            if amount <= self.admin_deposit_limit and (self.users[user_id]['balance'] + amount) <= self.admin_deposit_limit:
                self.users[user_id]['balance'] += amount
                print(f"Admin deposit successful. New balance for {user_id}: {self.users[user_id]['balance']} INR")
            else:
                print(f"Admin deposit rejected. Amount exceeds limit of {self.admin_deposit_limit} INR.")
        else:
            print("Invalid admin credentials or user not found.")

    def admin_withdraw(self, admin_id, user_id, amount):
        if admin_id == self.admin_user['username'] and user_id in self.users:
            if amount <= self.withdraw_limit and amount <= self.users[user_id]['balance']:
                self.users[user_id]['balance'] -= amount
                print(f"Admin withdrawal successful. New balance for {user_id}: {self.users[user_id]['balance']} INR")
            else:
                print(f"Admin withdrawal rejected. Check amount or withdrawal limit of {self.withdraw_limit} INR.")
        else:
            print("Invalid admin credentials or user not found.")

# Create Bank instance
bank = Bank()

# Create Users with 50,000 INR balance
users_list = ["aryan1", "aryan2", "aryan3", "aryan4", "aryan5"]
password = "password"

for user_id in users_list:
    bank.create_account(user_id, password)

# Welcome Message
print("Welcome to the Aryan ATM Machine!")

while True:
    print("\nMain Menu:")
    print("1. Create Account")
    print("2. User Login")
    print("3. Admin Login")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        user_id = input("Enter user ID: ")
        password = input("Set your password: ")
        bank.create_account(user_id, password)
    elif choice == "2":
        user_id = input("Enter user ID: ")
        password = input("Enter password: ")
        if bank.login(user_id, password):
            print(f"Welcome, {user_id}!")
            while True:
                print("\nATM Menu:")
                print("1. Check Balance")
                print("2. Deposit Money")
                print("3. Withdraw Money")
                print("4. Send Money")
                print("5. Change Password")
                print("6. Convert to USD")
                print("7. Logout")
                user_choice = input("Enter your choice: ")

                if user_choice == "1":
                    print(f"Current Balance: {bank.check_balance(user_id)}")
                    if bank.check_balance(user_id) < 5000:
                        bank.send_notification_to_admin(user_id)
                elif user_choice == "2":
                    amount = float(input("Enter the amount to deposit: "))
                    bank.deposit(user_id, amount)
                elif user_choice == "3":
                    amount = float(input("Enter the amount to withdraw: "))
                    bank.withdraw(user_id, amount)
                elif user_choice == "4":
                    recipient_id = input("Enter recipient user ID: ")
                    amount_to_send = float(input("Enter the amount to send: "))
                    bank.send_money(user_id, recipient_id, amount_to_send)
                elif user_choice == "5":
                    new_password = input("Enter your new password: ")
                    bank.change_password(user_id, new_password)
                elif user_choice == "6":
                    bank.convert_to_usd(user_id)
                elif user_choice == "7":
                    print(f"Goodbye, {user_id}!")
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid login credentials or user is blocked. Please try again.")
    elif choice == "3":
        admin_username = input("Enter admin username: ")
        admin_password = input("Enter admin password: ")
        if bank.admin_login(admin_username, admin_password):
            print(f"Welcome, {admin_username} (Admin)!")
            while True:
                print("\nAdmin Menu:")
                print("1. Block User")
                print("2. Unblock User")
                print("3. View User Information")
                print("4. View Notifications")
                print("5. Admin Deposit")
                print("6. Admin Withdraw")
                print("7. Exit Admin Menu")
                admin_choice = input("Enter your choice: ")

                if admin_choice == "1":
                    user_to_block = input("Enter the user ID to block: ")
                    bank.block_user(admin_username, user_to_block)
                elif admin_choice == "2":
                    user_to_unblock = input("Enter the user ID to unblock: ")
                    bank.unblock_user(admin_username, user_to_unblock)
                elif admin_choice == "3":
                    print("User Information:")
                    for user_id, user_info in bank.users.items():
                        print(f"User ID: {user_id}, Balance: {user_info['balance']}, Blocked: {user_info['blocked']}")
                elif admin_choice == "4":
                    bank.view_notifications()
                elif admin_choice == "5":
                    user_id = input("Enter user ID: ")
                    deposit_amount = float(input("Enter the amount to deposit: "))
                    bank.admin_deposit(admin_username, user_id, deposit_amount)
                elif admin_choice == "6":
                    user_id = input("Enter user ID: ")
                    withdraw_amount = float(input("Enter the amount to withdraw: "))
                    bank.admin_withdraw(admin_username, user_id, withdraw_amount)
                elif admin_choice == "7":
                    print(f"Goodbye, {admin_username} (Admin)!")
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid admin credentials. Access denied.")
    elif choice == "4":
        print("Thank you for using the Aryan ATM Machine. Goodbye!")
        break
    else:
        print("Not a valid choice. Please try again.")




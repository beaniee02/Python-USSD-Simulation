import mysql.connector as sql
import random
import sys
from dotenv import load_dotenv
import os

load_dotenv()

class Bank:
# Establishes the database connection and creates the table if it doesnt exist.
    def __init__(self):
        self.my_con = sql.connect(host = os.getenv("DB_HOST"), 
                                username = os.getenv("DB_USER"), 
                                password = os.getenv("DB_PASSWORD"), 
                                db = os.getenv("DB_NAME"))

        self.my_cursor = self.my_con.cursor()

        self.my_cursor.execute("CREATE TABLE IF NOT EXISTS register(customer_id INT(2) PRIMARY KEY AUTO_INCREMENT, fname VARCHAR(20), lname VARCHAR(20), dob VARCHAR(8), phonenum VARCHAR(11), email VARCHAR(50), residential_address VARCHAR(50))")
        self.my_con.commit()



        # self.my_cursor.execute('ALTER TABLE register ADD balance INT(5)')
        # self.my_con.commit()
        # print('column renamed successfully')

        # self.my_cursor.execute('ALTER TABLE register ADD PIN INT(4) UNIQUE')
        # self.my_con.commit()
        # print('column added successfully')

        # self.my_request = "SELECT * FROM register"
        # self.my_cursor.execute(self.my_request)
        # for each in self.my_cursor.fetchall():
        #     print(each)

        # self.my_query = "UPDATE register SET balance = 20000, PIN = 1903 WHERE email=%s"
        # self.my_val = ('jibola@gmail.com', )
        # self.my_cursor.execute(self.my_query, self.my_val)
        # self.my_con.commit()
        # print('jibola"s balance is updated successfully')

        # self.query = "DELETE FROM register WHERE email=%s"
        # self.val = ('busolami@gmail.com',)
        # self.my_cursor.execute(self.query, self.val)
        # self.my_con.commit()
        # print('record deleted successfully')

# This prompts the customer to choose between registration and logging in.
    def prompt(self):
        print('''
                    1. Register
                    2. Login
            ''')
        self.ask = input('Enter the number of the operation you want to perform>>> ')
        if self.ask == '1':
            return self.register()
        elif self.ask == '2':
            return self.login()
        else:
            return self.prompt()

# This function works to collect customer details, validating input and creating an account.
    def register(self):
        self.first_name = input('Enter your first name>>> ').strip()
        self.last_name = input('Enter your last name>>> ').strip()
        self.date_of_birth = input('Enter your date of birth(YY-MM-DD)>>> ').strip()
        
        while True:
            self.contact = input('Enter your phone number>>> ')
            if len(self.contact) == 11 and self.contact.isdigit():
                break
            else:
                print('Invalid phone number. It must be 11 digits')
        
        self.email = input('Enter your email address>>> ').strip()
        self.address = input('Enter your residential address>>> ').strip()
        self.random_acct = random.randint(00000000, 99999999)
        self.account = f'20{self.random_acct}'
        print('To activate your account, you have to make a deposit of at least N2000')
        while True:
            try:
                self.deposit_amount = int(input('How much do you want to deposit? '))
                if self.deposit_amount >= 2000:
                    print(f'You have deposited a sum of {self.deposit_amount} into your account')
                    break
                else:
                    print('The minimum amount you can deposit is N2000')
            except ValueError:
                print('You have entered an invalid amount')

        while True:
            try:
                self.pin = int(input('Create a 4 digit pin that you will be using for your ATM/ONLINE transactions>>> '))
                if len(str(self.pin)) == 4:
                    print('You have successfully created a pin for your transactions.')
                    break
                else:
                    print('Your pin must be exactly 4 digis.')
            except ValueError:
                print('Invalid pin! The use of alphabet is not allowed in the creation of your pin')

# Inserts the collected details into the database.
        self.my_query = "INSERT INTO register(fname, lname, dob, phonenum, email, residential_address, accountnum, balance, PIN) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.user_info= (self.first_name, self.last_name, self.date_of_birth, self.contact, self.email, self.address, self.account, self.deposit_amount, self.pin)

        try:
            self.my_cursor.execute(self.my_query, self.user_info)
            self.my_con.commit()
            print(f'Dear {self.first_name} {self.last_name}, you have successfully opened an account with our bank and your account number is {self.account}.')
        except sql.Error as e:
            print(f'Error: {e}')

# Prompts the customer on whether they want to log in after creatimg an acount.
        self.pre_login = input('Do you want to login into your account?(Yes/No) ')
        if self.pre_login == "yes":
            return self.login()
        if self.pre_login == "no":
            sys.exit()

# Prompts the customer on whwther they want to perform USSD or ATM banking.
    def login(self):
        print('''
                    1. USSD
                    2. ATM
            ''')
        self.prompt_user = input('Enter the number of the operation you want to perform>>> ')
        if self.prompt_user == '1':
            ussd_inst = Ussd()
            ussd_inst.dial()
        elif self.prompt_user == '2':
            pass
        
# The USSD Banking.
class Ussd(Bank):
    def __init__(self):
        super().__init__()

        
    def dial(self):
        while True:
            self.press = input('Dial *202# to start your USSD Banking>>> ')
            if self.press == '*202#':
                self.ussd_home()
                break
            else:
                print('You have entered an invalid USSD number')
                
# Prompts the customer on the type of transaction they want to make.
    def ussd_home(self):
        print('''
                    1. Buy Airtime
                    2. Buy Data
                    3. Transfers
                    4. Check Balance
            ''')
        
        while True:
            self.prompt_user = input('Enter the number of the operation you want to perform>>> ')
            if self.prompt_user == '1':
                self.check_number()
                self.airtime()
            elif self.prompt_user == '2':
                self.check_number()
                self.data()
            elif self.prompt_user == '3':
                self.check_number()
                self.transfer()
            elif self.prompt_user == '4':
                self.check_number()
                self.check_balance()
                break
            else:
                print('Invalid number')
                return self.ussd_home()

# Verifying that the phone number belongs to a registered customer.
    def check_number(self):
        while True:
            self.number = (input('Enter your number to continue USSD Banking>>> '))

            if not self.number.isdigit() or len(self.number) != 11:
                print ("Invalid Number. Please enter an 11-digit number.")
                continue

            self.number_val = (f'{self.number}', )
            self.check = 'SELECT phonenum FROM register WHERE phonenum=%s'

            try:
                self.my_cursor.execute(self.check, self.number_val)
                self.user_number = self.my_cursor.fetchone()

                if self.user_number:
                    self.pin()
                    break
                else:
                    print('''
                                You do not have an account.
                        ''')
                    #Redirects the customer to the registaration page supposed they are not a registered user.
                    self.register_account = input('Press 1 if you want to open an account>>> ')
                    if self.register_account == '1':
                        return self.register()
                    else:
                        print('You have entered an invalid number')
                        sys.exit()
            except sql.Error as e:
                print(f'Error: {e}')

        
# Authenticating the customer before allowing transactions.
    def pin(self):
        while True:
            try:
                self.pin_prompt = int(input('''
                                            Please enter your pin
                                                0. Back
                                '''))
                self.check_pin = 'SELECT phonenum, PIN FROM register where phonenum=%s AND PIN=%s'
                self.pin_val = (self.number, self.pin_prompt)
                self.my_cursor.execute(self.check_pin, self.pin_val)
                self.user_pin = self.my_cursor.fetchone()
                break
            except ValueError:
                print('You have entered an invalid PIN')
        
        try:
            if self.user_pin:
                pass
            else:
                print('Invalid PIN')
                return self.pin()
        except sql.Error as e:
            print(f'Error: {e}')

#  Allows the customer to choose an airtime purchase recipient
    def airtime(self):
        self.airtime_prompt = input('''
                            1. Airtime-Self
                            2. Airtime-Others
                        ''')
        if self.airtime_prompt == '1':
            self.airtime_amount()
        elif self.airtime_prompt == '2':
            self.destination_num = self.destination()

            if self.destination_num:
                self.airtime_amount()

        else:
            return self.airtime()

# Validating the amount and processing an airtime purchase.
    def airtime_amount(self):
        while True:
            self.airtimeAmount = input('''
                        Please enter amount (50 - 10000)
                        00. Back
                        0. Main
                    ''')
            if self.airtimeAmount == '00':
                self.airtime()
            elif self.airtimeAmount == '0':
                self.ussd_home()
            
            try:
                self.buyAirtime = int(self.airtimeAmount)
                if not 50 <= self.buyAirtime <= 10000:
                    print('Please enter a valid amount between 50 and 10000')
                else:
                    break
            except ValueError:
                print('Invalid amount.')

# Checks if the customer's balance is enough to process the transaction.
        self.check_balance_query = "SELECT balance FROM register WHERE phonenum=%s"
        self.my_cursor.execute(self.check_balance_query, (self.number,))
        self.current_balance = self.my_cursor.fetchone()

        if self.current_balance:
            self.current_balance = self.current_balance[0]

            if self.buyAirtime <= self.current_balance:
                self.new_balance = self.current_balance - self.buyAirtime
                self.update_balance_query = "UPDATE register SET balance=%s WHERE phonenum=%s"
                self.newquery = (self.new_balance, self.number)
                self.my_cursor.execute(self.update_balance_query, self.newquery)
                self.my_con.commit()
                self.processed()
            else:
                print('Insufficient funds')
                return sys.exit()
        else:
            print('Account not found')
    
# Collects and validates the recipient's phone number.
    def destination(self):
        while True:
            try:
                self.destination_num = (input('''
                                                Please enter destination phone line
                                                        0. Main
                                            '''))
                if self.destination_num == '0':
                    self.ussd_home()
                elif self.destination_num.isdigit() and len(self.destination_num) == 11:
                    #self.airtime_amount()
                    return self.destination_num
                    #break
                else:
                    print("Invalid number")

            except ValueError:
                print("Invalid number")

# Allows the customer to choose a data purchase recipient
    def data(self):
        self.dataprompt = input('''
                            1. Data-Self
                            2. Data-Others
                        ''')
        if self.dataprompt == '1':
            return self.data_amount()
        elif self.dataprompt == '2':
            self.destination_num = self.destination()

            if self.destination_num:
                self.data_amount()

# Displays the available data bundles and handle's the customer selection.
    def data_amount(self):
        self.data_prices = {
        '1': 100,
        '2': 100,
        '3': 1000,
        '4': 10000,
        '5': 10000
    }
        while True:
            self.buyData = input('''
                                Please select
                                    1. 1GB(Night5Days) N100
                                    2. 150MB(1day) N100
                                    3. 2.9GB(30days) N1000
                                    4. N10000 Oneoff(50GB) N10000
                                    5. 50GB(30days) N10000
                                            6. Next
                                            00. Back
                                            0. Main
                        ''')
            if self.buyData == '6':
                self.Data_Next()
            elif self.buyData == '00':
                self.pin()
                self.data()
            elif self.buyData == '0':
                self.ussd_home()

            elif self.buyData not in self.data_prices:
                print("Invalid option. Please select a valid data bundle.")
                continue
            
            # Sets the price of the selected bundle
            self.amount = self.data_prices[self.buyData]

            return self.process_data_purchase()

# Checks the customer balance and deduct the data bundle cost.
    def process_data_purchase(self):
        #Retrieve the current balance of the customer making the purchase.
        self.check_balance_query = "SELECT balance FROM register WHERE phonenum=%s"
        self.my_cursor.execute(self.check_balance_query, (self.number,))
        self.current_balance = self.my_cursor.fetchone()

        if self.current_balance is not None:
            self.current_balance = self.current_balance[0]

            # Deducts the selected data bundle from the customer's current balance
            if self.current_balance >= self.amount:
                self.new_balance = self.current_balance - self.amount

                # Updates the customer's balance after the transaction has been performed.
                self.update_balance_query = "UPDATE register SET balance=%s WHERE phonenum=%s"
                self.newquery = (self.new_balance, self.number)
                self.my_cursor.execute(self.update_balance_query, self.newquery)
                self.my_con.commit()
                    
                self.processed()
            else:
                print('Insufficient funds')
                return sys.exit()
        else:
            print('Account not found')

# Displays the next available data bundles and handle's the customer selection.
    def Data_Next(self):
        self.Nextdata_prices = {
        '1': 100000,
        '2': 1100,
        '3': 1500,
        '4': 1500,
        '5': 15000
    }
        while True:
            self.next_option = input('''
                                1. GloMega100000 oneoff(1TB) N100000
                                2. 5GB(30Days) N1100
                                3. 4.1GB(30Days) N1500
                                4. 7GB(7Days) N1500
                                5. N15000 Oneoff(93GB) N15000
                                        00. Back
                                        0. Main
                        ''')
            
            if self.next_option == '00':
                return self.data_amount()
            elif self.next_option == '0':
                self.ussd_home()
            elif self.next_option not in self.Nextdata_prices:
                print("Invalid option. Please select a valid data bundle.")
                continue

            # Sets the price of the selected bundle
            self.amount = self.Nextdata_prices[self.next_option]
            
            return self.process_data_purchase()

# Prompts the customer on the type of bank they want to make a trasanction to.
    def transfer(self):
        self.chooseBank = input('''
                                1. Trsf-UBA
                                2. Trsf- Other Banks
                                3. Trsf- MFB/others
                            ''')
        if self.chooseBank == '1':
            self.transfer_prompt()
        if self.chooseBank == '2':
            self.choose_otherbank()
        if self.chooseBank == '3':
            self.choose_mfbbank()
        else:
            print('Invalid number')

#Collects and verifies recipient's account details.
    def transfer_prompt(self):
        while True:
            self.destination_acct = input('Please enter Beneficiary Account Number>>> ')
            if not self.destination_acct.isdigit():    #This line of code is to catch errors of when the user mistakenly types an alphabet or symbol.
                print("Invalid input. Please enter digits only.")
                continue

            if len(self.destination_acct) == 10:
                self.transfer_amount()
                break
            else:
                print("Incorrect account number. Please enter correct account number to proceed.>>>")
                continue
        
# Prompts the customer to choose the commercial bank the recipient uses.
    def choose_otherbank(self):
        while True:
            self.ask_bank = input('''
                                    Please select Bank:
                                        1. First Bank of Nigeria
                                        2. Access Bank
                                        3. Zenith Bank
                                        4. GTB
                                        5. Wema
                            ''')
            if self.ask_bank in ('1', '2', '3', '4', '5'):
                self.transfer_prompt()
                break
            else:
                print("Invalid number. Please enter number from the list of options above")

# Prompts the customer to choose the microfinance bank the recipient uses.
    def choose_mfbbank(self):
        while True:
            self.askbank = input('''
                                    Please select Bank:
                                        1. Paycom(Opay)
                                        2. Moniepont
                                        3. Kuda micfrfinance bank
                                        4. Palmpay
                            ''')
            if self.askbank in ('1', '2', '3', '4'):
                self.transfer_prompt()
                break
            else:
                print("Invalid number. Please enter number from the list of options above")

# Validates the transfer amount and updates the customer's balance.
    def transfer_amount(self):
        self.amount = int(input('Please enter amount>>> '))
        self.check_balance_query = "SELECT balance FROM register WHERE phonenum=%s"
        self.my_cursor.execute(self.check_balance_query, (self.number,))
        self.current_balance = self.my_cursor.fetchone()

        if self.current_balance:
            self.current_balance = self.current_balance[0]

            if self.amount <= self.current_balance:    
                self.new_balance = self.current_balance - self.amount
                self.update_balance_query = "UPDATE register SET balance=%s WHERE phonenum=%s" 
                self.newquery = (self.new_balance, self.number)
                self.my_cursor.execute(self.update_balance_query, self.newquery)
                self.my_con.commit()
                self.processed()
            else:
                print('Insufficient funds')
                return sys.exit()
        else:
            print('Account not found')

# Charges the customer a service fee and displays their balance.
    def check_balance(self):
        self.checkbalance = input('''
                                Transaction fee of N20.00 applies.
                                    Do you wish to continue?
                                            1. Yes
                                            2. No
                    ''')
        if self.checkbalance == '1':
            self.check_balance_query = "SELECT balance FROM register WHERE phonenum=%s"
            self.my_cursor.execute(self.check_balance_query, (self.number,))
            self.current_balance = self.my_cursor.fetchone()

            if self.current_balance:
                self.current_balance = self.current_balance[0]

                if self.current_balance:
                    self.new_balance = self.current_balance - 20 
                    self.update_balance_query = "UPDATE register SET balance=%s WHERE phonenum=%s" 
                    self.newquery = (self.new_balance, self.number)
                    self.my_cursor.execute(self.update_balance_query, self.newquery)
                    self.my_con.commit()
                    print(f'you have a total of {self.new_balance} naira in your account.')
                else:
                    print('Insufficient funds')
                    return sys.exit()
            else:
                print('Account not found')
                return sys.exit()
        elif self.checkbalance == '2':
            sys.exit()

# Informs the customer of every successful transaction oucome.
    def processed(self):
        print('Transaction is being processed.')
        return sys.exit()






bank_inst = Bank()
bank_inst.prompt()
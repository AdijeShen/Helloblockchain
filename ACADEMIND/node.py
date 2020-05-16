from ACADEMIND.verification import Verification
from ACADEMIND.blockchain import Blockchain


def get_transaction_value():
    tx_recipient = input("Enter the recipient of the transaction: ")
    user_input = float(input("Your transaction mount: "))
    return tx_recipient, user_input


def get_user_choice():
    user_input = input("Your Choice:")
    return user_input


def get_user_input():
    return input("Input the transaction amount: ")


class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = "Adije"
        self.blockchain = Blockchain(self.id)

    def print_blockchain_elements(self):
        """
        Print the blockchain list to the console
        """
        print('-' * 30)
        for block in self.blockchain.chain:
            print('Outputting Block')
            print(block)
        print('-' * 30)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print("Please choose")
            print("1: Add a new transaction value")
            print("2: Mine a new block")
            print("3: Output the blockchain blocks")
            print("4: Check transaction validity")
            print("q: Quit")
            user_choice = get_user_choice()
            if user_choice == "1":
                recipient, amount = get_transaction_value()
                if self.blockchain.add_transaction(sender=self.id, recipient=recipient, amount=amount):
                    print("Added transaction!")
                else:
                    print("Transaction Fail!")
                print(self.blockchain.get_open_transactions())
            elif user_choice == "2":
                self.blockchain.mine_block()
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if Verification.verify_transactions(self.blockchain.get_open_transactions(),
                                                    self.blockchain.get_balance):
                    print("Transactions all valid")
                else:
                    print("There are invalid transactions")
            elif user_choice == "q":
                waiting_for_input = False
            else:
                print("Input is invalid, please pick a value from the list!")
            if not Verification.verify_blockchain(self.blockchain.chain):
                print("Invalid blockchain!")
                break
            print("Balance of {}:{:6.2f}".format(self.id, self.blockchain.get_balance()))
        else:
            print("User left")
        print("Done!")


node = Node()
node.listen_for_input()

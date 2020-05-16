from ACADEMIND.utility.hash_util import hash_string_256, hash_block
from ACADEMIND.transaction import Transaction


class Verification:

    @staticmethod
    def valid_proof(transactions: [Transaction], last_hash, proof):
        """
        Check whether a proof is validate.
        :param transactions:
        :param last_hash:
        :param proof:
        :return:
        """
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode('utf-8')
        guess_hash = hash_string_256(guess)
        return guess_hash.startswith("00")

    @classmethod
    def verify_blockchain(cls, blockchain):
        """
        :return: The validity of blockchain
        """
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if hash_block(blockchain[index - 1]) != block.previous_hash:
                print("The hash of previous block is not correct!")
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid!")
                return False
        return True

    @staticmethod
    def verify_transaction(transaction: Transaction, get_balance):
        """Check if the sender have enough balance for this transaction"""
        sender_balance = get_balance()
        return sender_balance >= transaction.amount

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """verify all the open transactions"""
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])

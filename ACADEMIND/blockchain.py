from functools import reduce
import json
from ACADEMIND.utility.hash_util import hash_block
from ACADEMIND.block import Block
from ACADEMIND.transaction import Transaction
from ACADEMIND.utility.verification import Verification

MINING_REWARD = 10.0


class Blockchain:
    _chain: [Block]

    def __init__(self, hosting_node_id):
        # Unhandled transactions
        self.__open_transactions = []
        genesis_block = Block(0, '', [], 0)
        # Initializing the blockchain list
        self.chain = [genesis_block]
        self.load_data()
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self._chain[:]

    @chain.setter
    def chain(self, value):
        self._chain = value

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())

                file_content = f.readlines()

                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in
                                    block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'],
                                          block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain[:]
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions[:]
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                savable_chain = [block.__dict__ for block in [
                    Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions],
                          block_el.proof, block_el.timestamp) for block_el in self._chain]]
                f.write(json.dumps(savable_chain))
                f.write('\n')
                savable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(savable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print("Saving Failed!")

    def proof_of_work(self):
        """Generate a proof of work for the candidate block"""
        last_block = self._chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        """
        :return: The remaining balance of the node
        """
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self._chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx: tx_sum + sum(tx) if len(tx) > 0 else tx_sum + 0, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in
                        self._chain]
        amount_received = reduce(lambda tx_sum, tx: tx_sum + sum(tx) if len(tx) > 0 else tx_sum + 0, tx_recipient,
                                 0)
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        """
        :return: Returns the last value of the current blockchain.
        """
        if len(self._chain) < 1:
            return None
        else:
            return self._chain[-1]

    def add_transaction(self, sender, recipient, amount=1.0):
        """
        Append a new transaction to the blockchain.
        :param sender:
        :param recipient:
        :param amount:
        :return:
        """
        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount
        # }
        if self.hosting_node is None:
            return False
        transaction = Transaction(sender, recipient, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        else:
            return False

    def mine_block(self):
        if self.hosting_node is None or self.chain is None:
            return False
        last_block = self._chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self._chain), hashed_block, copied_transactions, proof)
        self._chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True

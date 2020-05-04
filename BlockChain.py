from Block import *


class BlockChain:
    blocks = []

    def __init__(self):
        self.blocks = [create_genesis_block()]

    def add_block(self, data):
        """
        在区块链中添加一个新区块并返回
        :param data:新区快中的数据
        :return: 返回一个新区快
        """
        prev_block = self.blocks[len(self.blocks) - 1]
        new_block = Block(id=len(self.blocks), data=data, prev_hash=prev_block.hash)
        pow = ProofOfWork(new_block)
        nonce, digest = pow.mine()
        new_block.nonce = nonce
        self.blocks.append(new_block)
        print(new_block)
        return new_block

    def __str__(self):
        """
        用一个形式化大的输出字符串来打印Blockchain
        :return: 返回形式化的输出字符串
        """
        result = "Blockchain data is:\n"
        for index in range(len(self.blocks)):
            result += "%s\n" % (self.blocks[index])
        return result


bc = BlockChain()
print(bc)
bc.add_block("Jack send 0.3 btc to Alice")
bc.add_block("Alice send 0.1 btc to Tom")
bc.add_block("Jack send 0.1 btc to Tom")
bc.add_block("Tom send 0.1 btc to Alice")
bc.add_block("Alice send 0.1 btc to Jack")
bc.add_block("Tom send 0.1 btc to Jack")

# print("If we change the content in block 1")
# bc.blocks[1].data="Jack send 0.1 btc to Alice"
# print(bc)

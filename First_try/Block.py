import hashlib
import time
import random


class Block:
    nonce: str
    data = []
    previous_hash: str
    id: int

    def __init__(self, id, data, prev_hash):
        """
        初始化一个区块
        :param id: 当前区块的id
        :param data: 当前区块的数据
        :param prev_hash: 前一个区块的哈希值
        """
        self.id = id
        self.data = data
        self.previous_hash = prev_hash
        self.nonce = ""

    @property
    def hash(self):
        """
        使用SHA-256哈希函数来对区块自身进行哈希运算
        :return:返回哈希值
        """
        message = hashlib.sha256()
        message.update(str(self.data).encode('utf-8'))
        message.update(str(self.nonce).encode('utf-8'))
        return message.hexdigest()

    def __str__(self):
        """
        标准化输出block
        :return: 返回标准化输出结果
        """
        return "Block ID: %d,\nPrevious Hash: %s,\nCurrent Hash: %s,\nNonce: %s,\nData: %s\n" % (
            self.id, self.previous_hash, self.hash, self.nonce, self.data)


class ProofOfWork():
    """
    工作量证明
    """
    block: Block

    def __init__(self, block):
        self.block = block

    def mine(self):
        """
        挖矿
        :return:
        """
        start_time = time.clock()
        i = 0
        prefix = "0000"
        print("Mining...")
        while True:
            nonce = str(int(random.randint(0,100000000000000000000000000)))
            message = hashlib.sha256()
            message.update(str(self.block.data).encode('utf-8'))
            message.update(nonce.encode("utf-8"))
            digest = message.hexdigest()
            if digest.startswith(prefix):
                finish_time = time.clock()
                print("finished in %s s" % (finish_time - start_time))
                return nonce, digest
            i += 1


def create_genesis_block():
    """
    创建一个新区快
    :return: 返回新区快
    """
    block = Block(id=0, data="Genesis Block", prev_hash="")
    pow = ProofOfWork(block)
    nonce, digest = pow.mine()
    block.nonce = nonce
    return block

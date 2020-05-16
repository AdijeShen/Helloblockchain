import hashlib as hl
import json
from ACADEMIND.block import Block


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block: Block):
    """
    :param block: The block data
    :return: The hash value of this block
    """
    # string = (str(block['transactions'][:-1]) + str(block['previous_hash']) + str(block['proof'])).encode('utf-8')
    # return hl.sha256(string).hexdigest()
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode('utf-8'))

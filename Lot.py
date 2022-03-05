from BlockchainUtils import BlockchainUtils


class Lot:
    def __init__(self, publicKey, iteration, lastBlockHash):

        # publicKey: corresponding to staker who wants to create the lot
        # iteration: amount of tokens staked defines the amount of iterations => amount of lots

        self.publicKey = str(publicKey)
        self.iteration = iteration
        self.lastBlockHash = lastBlockHash

    def lotHash(self):

        # create hash and lots

        hashData = self.publicKey + self.lastBlockHash  # lot is based on both
        # as many iterations as defined by iteration prop, need no value
        for _ in range(self.iteration):
            ## *HASH_CHAINING* with non-fixed iterations -> create different lots
            # iterate hash over result of last hash operation
            hashData = BlockchainUtils.hash(hashData).hexdigest()
        return hashData

    """
    The reason why we use *HASH_CHAINING* (with non-fixed iterations) is to create different lots.
    If we would use a fixed value, all the lots per staker would have the exact same hash value.
    This way, a higher stake would not lead to better chances of becoming the next forger as all lots would be the same.
    In other words the offset from all staker's lots to the target lot would be the same.

    So summed up, we don't only have to make sure that the amount of generated lots per staker is equivalent to it's stake,
        we also have to make sure that all the lots are different.
    """

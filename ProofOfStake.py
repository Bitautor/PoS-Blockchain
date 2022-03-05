from Lot import Lot
from BlockchainUtils import BlockchainUtils


class ProofOfStake:

    # keep track of the stake that is staked by a certain account

    def __init__(self):
        self.stakers = {}  # mapping 'stakers_account_key : amount_of_stake'
        self.setGenesisNodeStake()

    def setGenesisNodeStake(self):
        # setting first node stake to solf the problem of the first forger in the system
        # get genesis PUBLIC KEY from 'genesisPublicKey' file
        # safe first forger in stakers dictionary
        genesisPublicKey = open("keys/genesisPublicKey.pem", "r").read()
        self.stakers[genesisPublicKey] = 1

    def update(self, publicKeyString, stake):
        if publicKeyString in self.stakers.keys():
            # update stakers staking value
            self.stakers[publicKeyString] += stake
        else:
            # add new staker with corresponding stake
            self.stakers[publicKeyString] = stake

    def get(self, publicKeyString):
        # read out amount of stake an account holds
        if publicKeyString in self.stakers.keys():
            return self.stakers[publicKeyString]
        else:
            # provided publicKeyString not corresponding to a staker
            return None

    def validatorLots(self, seed):
        # generating all the lots for validator
        # seed: lastBlockHash
        lots = []
        for validator in self.stakers.keys():
            for stake in range(self.get(validator)):
                # int stake: number of tokens staked by validator
                # value staked => number of lots
                lots.append(Lot(validator, stake + 1, seed))
        return lots

    def winnerLot(self, lots, seed):
        # comparing all lots with the referece hash
        # the lot with the least offset to the referece hash is the WINNER
        winnerLot = None
        leastOffset = None
        # create reference hash from seed (16 bytes int)
        referenceHashIntValue = int(BlockchainUtils.hash(seed).hexdigest(), 16)
        for lot in lots:
            lotIntValue = int(lot.lotHash(), 16)
            offset = abs(
                lotIntValue - referenceHashIntValue
            )  # absolute distance to reference hash
            if leastOffset is None or offset < leastOffset:
                # update leastOffset and set winnerLot
                leastOffset = offset
                winnerLot = lot
        return winnerLot

    def forger(self, lastBlockHash):
        lots = self.validatorLots(lastBlockHash)  # lots from all stakers
        winnerLot = self.winnerLot(lots, lastBlockHash)
        return winnerLot.publicKey

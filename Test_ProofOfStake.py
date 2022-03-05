import string
import random
from ProofOfStake import ProofOfStake


def getRandomString(length):
    letters = string.ascii_lowercase
    resultString = "".join(random.choice(letters) for i in range(length))
    return resultString


## TESTING:
# test if the chance to be chosen as validator corresponds to the amount of staked tokens

if __name__ == "__main__":  # ENTRY POINT
    pos = ProofOfStake()
    pos.update("bob", 10)
    pos.update("alice", 100)

    bobWins = 0
    aliceWins = 0

    for i in range(100):
        forger = pos.forger(getRandomString(i))
        if forger == "bob":
            bobWins += 1
        elif forger == "alice":
            aliceWins += 1

    print("bob won " + str(bobWins) + " times")
    print("alice won " + str(aliceWins) + " times")

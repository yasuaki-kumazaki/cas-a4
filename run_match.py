from shared.match import IteratedMatch, MatchConfig
from strategies.random_bid import RandomBid
from strategies.team_g2 import G2
from strategies.team_g7 import G7

"""
Entry point.

Change:
- N
- rounds
- strategies A / B

to test different setups.
"""
def main():
    cfg = MatchConfig(N=5, rounds=10, verbose=True)
    A = G2()
    #A = G7()
    B = RandomBid()

    scoreA, scoreB = IteratedMatch(A, B, cfg).run()
    print("=== 1v1 Result ===")
    print(A.name, scoreA)
    print(B.name, scoreB)

if __name__ == "__main__":
    main()

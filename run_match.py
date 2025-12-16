from shared.match import MatchConfig
from tournament_core import make_strategies, print_leaderboard, run_tournament


def main():
    cfg = MatchConfig(N=100, rounds=1000, verbose=False)
    stats, h2h = run_tournament(make_strategies(), cfg, play_both_orders=False)
    print_leaderboard(stats)

if __name__ == "__main__":
    main()

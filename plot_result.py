import matplotlib.pyplot as plt
import numpy as np

from shared.match import MatchConfig
from tournament_core import make_strategies, print_leaderboard, run_tournament


def grouped_bar_plot(results, strategy_names, bar_keys, title, y_getter, ylabel):
    x = np.arange(len(strategy_names))
    width = 0.8 / max(1, len(bar_keys))

    plt.figure()
    for i, k in enumerate(bar_keys):
        stats_dict = results[k]
        ys = [y_getter(stats_dict[name], k) for name in strategy_names]
        plt.bar(x + i * width - 0.4 + width / 2, ys, width, label=str(k))

    plt.xticks(x, strategy_names, rotation=30, ha="right")
    plt.title(title)
    plt.ylabel(ylabel)
    plt.legend(title="Setting")
    plt.tight_layout()


def main():
    sweep_mode = "N"           # "N" or "rounds"
    play_both_orders = False

    results = {}

    if sweep_mode == "N":
        Ns = [10, 50, 100, 500, 1000]
        fixed_rounds = 1000

        for N in Ns:
            print(f"\n=== Running: N={N}, rounds={fixed_rounds} ===")
            cfg = MatchConfig(N=N, rounds=fixed_rounds, verbose=False)
            stats, _ = run_tournament(make_strategies(), cfg, play_both_orders=play_both_orders)
            results[N] = stats
            print_leaderboard(stats)

        strategy_names = [s.name for s in make_strategies()]
        grouped_bar_plot(results, strategy_names, Ns,
                         f"Wins (rounds={fixed_rounds})",
                         y_getter=lambda st, _k: st.wins,
                         ylabel="Wins")

        grouped_bar_plot(results, strategy_names, Ns,
                         f"Avg payoff/round (rounds={fixed_rounds})",
                         y_getter=lambda st, _k: st.points_for / fixed_rounds,
                         ylabel="Avg payoff per round")

        grouped_bar_plot(results, strategy_names, Ns,
                         f"Total payoff (rounds={fixed_rounds})",
                         y_getter=lambda st, _k: st.points_for,
                         ylabel="Total payoff")

    else:
        fixed_N = 50
        rounds_list = [50, 300, 1000]

        for r in rounds_list:
            print(f"\n=== Running: N={fixed_N}, rounds={r} ===")
            cfg = MatchConfig(N=fixed_N, rounds=r, verbose=False)
            stats, _ = run_tournament(make_strategies(), cfg, play_both_orders=play_both_orders)
            results[r] = stats
            print_leaderboard(stats)

        strategy_names = [s.name for s in make_strategies()]
        grouped_bar_plot(results, strategy_names, rounds_list,
                         f"Wins (N={fixed_N})",
                         y_getter=lambda st, _k: st.wins,
                         ylabel="Wins")

        grouped_bar_plot(results, strategy_names, rounds_list,
                         f"Avg payoff/round (N={fixed_N})",
                         y_getter=lambda st, r: st.points_for / r,
                         ylabel="Avg payoff per round")

        grouped_bar_plot(results, strategy_names, rounds_list,
                         f"Total payoff (N={fixed_N})",
                         y_getter=lambda st, _k: st.points_for,
                         ylabel="Total payoff")

    plt.show()
    return results


if __name__ == "__main__":
    main()

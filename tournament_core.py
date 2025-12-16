from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Tuple

from shared.match import IteratedMatch, MatchConfig
from strategies.team_g2 import G2
from strategies.team_g3 import G3
from strategies.team_g4 import G4
from strategies.team_g5 import G5
from strategies.team_g6 import Strategy6
from strategies.team_g7 import G7
from strategies.team_g8 import G8


def make_strategies():
    return [
        G2(),
        G3(),
        G4(),
        G5(),
        Strategy6(),
        G7(),
        G8(),
    ]


@dataclass
class Stats:
    points_for: float = 0.0
    points_against: float = 0.0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    matches: int = 0

    @property
    def diff(self) -> float:
        return self.points_for - self.points_against


def run_tournament(
    strategies,
    cfg: MatchConfig,
    play_both_orders: bool = False,
) -> Tuple[Dict[str, Stats], Dict[Tuple[str, str], Tuple[float, float]]]:
    stats: Dict[str, Stats] = {s.name: Stats() for s in strategies}
    h2h: Dict[Tuple[str, str], Tuple[float, float]] = {}

    def record(a_name: str, b_name: str, score_a: float, score_b: float):
        sa, sb = stats[a_name], stats[b_name]
        sa.points_for += score_a
        sa.points_against += score_b
        sa.matches += 1

        sb.points_for += score_b
        sb.points_against += score_a
        sb.matches += 1

        if score_a > score_b:
            sa.wins += 1
            sb.losses += 1
        elif score_a < score_b:
            sb.wins += 1
            sa.losses += 1
        else:
            sa.draws += 1
            sb.draws += 1

    for S1, S2 in combinations(strategies, 2):
        A = type(S1)()
        B = type(S2)()
        local_cfg = MatchConfig(N=cfg.N, rounds=cfg.rounds, verbose=False)

        scoreA, scoreB = IteratedMatch(A, B, local_cfg).run()
        record(A.name, B.name, scoreA, scoreB)
        h2h[(A.name, B.name)] = (scoreA, scoreB)

        if play_both_orders:
            A2 = type(S1)()
            B2 = type(S2)()
            scoreB2, scoreA2 = IteratedMatch(B2, A2, local_cfg).run()
            record(A2.name, B2.name, scoreA2, scoreB2)

            prev = h2h[(A.name, B.name)]
            h2h[(A.name, B.name)] = (prev[0] + scoreA2, prev[1] + scoreB2)

    return stats, h2h


def print_leaderboard(stats: Dict[str, Stats]):
    rows = []
    for name, st in stats.items():
        rows.append((name, st.wins, st.draws, st.losses, st.matches, st.points_for, st.points_against, st.diff))

    rows.sort(key=lambda r: (r[1], r[7], r[5]), reverse=True)

    print("\n=== Leaderboard ===")
    print(f"{'Strategy':<18} {'W':>3} {'D':>3} {'L':>3} {'M':>3} {'PF':>10} {'PA':>10} {'DIFF':>10}")
    for (name, w, d, l, m, pf, pa, diff) in rows:
        print(f"{name:<18} {w:>3} {d:>3} {l:>3} {m:>3} {pf:>10.2f} {pa:>10.2f} {diff:>10.2f}")

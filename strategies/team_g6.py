from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from shared.types import MatchResult, Observation


@dataclass
class _Mem:
    # Counts of opponent actions (index 0 -> bid 1)
    opp_counts: List[int]
    # Smoothed probability distribution over opponent bids
    opp_probs: List[float]


class Strategy6:
    """
    G6 Strategy (adapted to the course framework).

    Learns an opponent bid distribution online (Dirichlet/add-one smoothing),
    then chooses the bid that maximizes expected payoff:

        payoff(b) = b * P(opponent_bid > b)

    Uses epsilon-greedy to occasionally explore.
    """

    name = "G6"

    def __init__(self, *, epsilon: float = 0.15) -> None:
        self.N: int = 0
        self.epsilon = float(epsilon)
        self.mem: _Mem | None = None

    def reset(self, *, N: int) -> None:
        self.N = N
        self.mem = _Mem(
            opp_counts=[0 for _ in range(N)],
            opp_probs=[1.0 / N for _ in range(N)],
        )

    def act(self, obs: Observation) -> int:
        assert self.mem is not None

        # epsilon-greedy exploration
        if random.random() < self.epsilon:
            return random.randint(1, self.N)

        best_b = 1
        best_val = -1.0

        # suffix_gt[i] = P(opp > (i+1))
        suffix_sum = 0.0
        suffix_gt = [0.0] * self.N
        for i in range(self.N - 1, -1, -1):
            suffix_gt[i] = suffix_sum
            suffix_sum += self.mem.opp_probs[i]

        for i in range(self.N):  # i=0 -> bid 1
            b = i + 1
            val = b * suffix_gt[i]
            if val > best_val:
                best_val = val
                best_b = b

        return best_b

    def on_result(self, result: MatchResult) -> None:
        assert self.mem is not None

        opp_bid = result.opp_action
        if 1 <= opp_bid <= self.N:
            self.mem.opp_counts[opp_bid - 1] += 1

        # Dirichlet(1) prior (add-one smoothing)
        total = sum(self.mem.opp_counts) + self.N
        self.mem.opp_probs = [(c + 1) / total for c in self.mem.opp_counts]

from __future__ import annotations

from typing import Protocol

from shared.types import MatchResult, Observation
import random

class G8:
    """
    - name: str
    - reset(N)
    - act(obs) -> int
    - on_result(result)
    """
    name="G8"
    ALPHA = 0.8

    def __init__(self)->None:
        self.N = 0
        self.rounds_played = 0

    def reset(self, *, N: int) -> None:
        """
        Parameters:
        - N: number of possible bids (actions are 1..N)

        Use this to:
        - initialize internal state
        - reset memory / learning variables
        """
        self.N = N
        self.f = []
        self.rounds_played = 0

        self.wins = [0] * self.N


        for i in range(1, N + 1):
            if i <= N // 2:
                value = (2 / (N ** 2)) * i
            else:
                value = (2 / (N ** 2)) * (N - i + 1)
            self.f.append(value)

        #Normalization
        total = sum(self.f)
        self.f = [x / total for x in self.f]

    def act(self, obs: Observation) -> int:
        """
        Called EVERY round to choose a bid.

        Must return an integer in {1, 2, ..., N}.
        """
        actions = list(range(1, self.N + 1))
        choice = random.choices(actions, weights=self.f, k=1)[0]
        return choice

    def on_result(self, result: MatchResult) -> None:
        """
        Called AFTER each round.

        Use this to:
        - update memory
        - update learning statistics
        """
        self.rounds_played += 1

        if result.self_payoff > 0:
            self.wins[result.self_action - 1] += 1

        p_win = [
            self.wins[i] / self.rounds_played
            for i in range(self.N)
        ]


        self.f = [
            self.f[i] + self.ALPHA * p_win[i]
            for i in range(self.N)
        ]

        # Normalization
        total = sum(self.f)
        if total > 0:
            self.f = [fi / total for fi in self.f]

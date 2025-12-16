import random

from shared.types import MatchResult, Observation


class G5:
    name = "G5"

    def reset(self, *, N: int) -> None:
        self.N = N

        # Start with uniform distribution
        self.probs = [0.0] + [1.0 / N for _ in range(N)]

        self.last_self_action = None

        # print(f"[RESET] Initial distribution: {self._pretty_probs()}")

    def act(self, obs: Observation) -> int:
        r = random.random()
        cumulative = 0.0

        for i in range(1, self.N + 1):
            cumulative += self.probs[i]
            if r <= cumulative:
                self.last_self_action = i
                return i

        self.last_self_action = self.N
        return self.N

    def on_result(self, result: MatchResult) -> None:
        if result.self_payoff <= 0:
            return  # only update when G5 wins

        winning_value = self.last_self_action
        delta = 1.000 / (self.N * self.N)  # 1 / N^2

        for i in range(1, self.N + 1):
            if i != winning_value:
                self.probs[i] -= delta

        self.probs[winning_value] += (self.N - 1) * delta

        # DEBUG CHECK (optional but recommended)
        total = sum(self.probs[1:])
    #     print(
    #         f"[UPDATE] G5 WON with {winning_value} | "
    #         f"sum={round(total, 6)} | "
    #         f"{[round(self.probs[i], 4) for i in range(1, self.N + 1)]}"
    #  )





    def _pretty_probs(self):
        return [round(self.probs[i], 3) for i in range(1, self.N + 1)]

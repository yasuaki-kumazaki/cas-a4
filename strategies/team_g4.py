import random

from shared.types import Observation, MatchResult


class G4:
    name: str = 'G4'
    j : int
    totalRounds : int

    class Mode:
        AGGRESSIVE = 0
        NEUTRAL = 1
        PATIENT = 2

    def __init__(self) -> None:
        self.N = 0
        self.j = 0
        self.totalRounds = 0
        self.mode = self.Mode.NEUTRAL

    def reset(self, *, N: int) -> None :
        self.N = N
        self.j = 0
        self.totalRounds = 0
        self.mode = self.Mode.NEUTRAL
        return

    def act(self, obs: Observation) -> int:
        self.N = obs.N
        action: int
        if self.mode == self.Mode.AGGRESSIVE:
            action = self.act_aggressive()
        elif self.mode == self.Mode.NEUTRAL:
            action = self.act_neutral()
        else:
            action = self.act_patient()
        return action

    def on_result(self, result: MatchResult) -> None:
        if result.opp_action == 1:
            self.j += 1
        self.totalRounds += 1
        self.update_mode()
        return

    def update_mode(self) -> None:
        p = float(self.j) / float(self.totalRounds)
        if p < 0.35:
            self.mode = self.Mode.AGGRESSIVE
        elif p > 0.6:
            self.mode = self.Mode.PATIENT
        else:
            self.mode = self.Mode.NEUTRAL

    def act_aggressive(self) -> int:
        actions = list(range(1, self.N + 1))
        for i in range(self.N//2):
            actions[i] = 1.0 / pow(actions[i], 3)
        for i in range(self.N//2, self.N):
            actions[i] = 0.0
        distribution = self.calculate_distribution(actions)
        return self.calculate_action(distribution)

    def act_neutral(self) -> int:
        actions = list(range(1, self.N + 1))
        start = self.N // 4
        end = 3 * self.N // 4
        for i in range(start, end):
            actions[i] = 1.0 / pow(actions[i], 3)
        # alles andere = 0
        for i in range(0, start):
            actions[i] = 0.0
        for i in range(end, self.N):
            actions[i] = 0.0
        distribution = self.calculate_distribution(actions)
        return self.calculate_action(distribution)

    def act_patient(self) -> int:
        actions = list(range(1, self.N + 1))
        start = self.N // 2
        for i in range(start, self.N):
            actions[i] = 1.0 / pow(actions[i], 3)
        # alles andere = 0
        for i in range(0, start):
            actions[i] = 0.0
        distribution = self.calculate_distribution(actions)
        return self.calculate_action(distribution)

    def calculate_distribution(self, actions: list[int]) -> list[float]:
        total = sum(actions)
        return [x / total for x in actions]

    def calculate_action(self, distribution: list[float]) -> int:
        N = len(distribution)

        # Ziehe eine Aktion basierend auf Wahrscheinlichkeiten
        return random.choices(range(N), weights=distribution, k=1)[0] + 1

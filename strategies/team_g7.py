from __future__ import annotations

import math
import random
from collections import deque
from dataclasses import dataclass
from typing import Deque

from shared.types import MatchResult, Observation


@dataclass
class _Memory:
    """Internal memory for the G7 strategy"""
    state: str  
    payoff_history: Deque[int]  


class G7:

    name = "G7"

    
    ALPHA = 0.75  # SAFE distribution decay parameter
    BETA = 0.35   # RISKY distribution growth parameter

    # state transition thresholds from the report
    TAU_LOW = 2.5   
    TAU_HIGH = 4.0  
    TAU_VAR = 5.0  

    def __init__(self) -> None:
        self.N = 0
        self.mem: _Memory | None = None
        self.safe_dist: list[float] = []
        self.risky_dist: list[float] = []

    def reset(self, *, N: int) -> None:
        """Initialize for a new match"""
        self.N = N
        self.mem = _Memory(
            state="SAFE",  # Start in SAFE state
            payoff_history=deque(maxlen=3)  # Keep last 3 payoffs for transition logic
        )

        # Precompute the probability distributions
        self._compute_distributions()

    def _compute_distributions(self) -> None:
        # dictates the use of safe or risky tatctin
        # SAFE distribution (favors low values)
        safe_unnormalized = [math.exp(-self.ALPHA * i) for i in range(1, self.N + 1)]
        safe_sum = sum(safe_unnormalized)
        self.safe_dist = [p / safe_sum for p in safe_unnormalized]

        # RISKY distribution (favors high values)
        risky_unnormalized = [math.exp(self.BETA * i) for i in range(1, self.N + 1)]
        risky_sum = sum(risky_unnormalized)
        self.risky_dist = [p / risky_sum for p in risky_unnormalized]

    def _sample_from_distribution(self, distribution: list[float]) -> int:
        r = random.random()
        cumulative = 0.0

        for i, prob in enumerate(distribution):
            cumulative += prob
            if r < cumulative:
                return i + 1  # Actions are 1-indexed

        return self.N  # Fallback (should not happen with proper probabilities)


    #called for every round
    def act(self, obs: Observation) -> int:
        assert self.mem is not None

        if self.mem.state == "SAFE":
            return self._sample_from_distribution(self.safe_dist)
        else:  # RISKY
            return self._sample_from_distribution(self.risky_dist)


    def on_result(self, result: MatchResult) -> None:
        assert self.mem is not None

        # Store the payoff from this round
        self.mem.payoff_history.append(result.self_payoff)

        # 3 rounds needed for study
        if len(self.mem.payoff_history) < 3:
            return

        # Compute mean of last 3 payoffs
        payoffs = list(self.mem.payoff_history)
        mu = sum(payoffs) / 3.0

        # Compute variance of last 3 payoffs
        variance = sum((p - mu) ** 2 for p in payoffs) / 3.0
        sigma = math.sqrt(variance)

        # State transition logic
        # Switch to SAFE if performance is poor OR unstable
        if mu < self.TAU_LOW or sigma > self.TAU_VAR:
            self.mem.state = "SAFE"

        # Switch to RISKY if performance is good AND stable
        elif mu > self.TAU_HIGH and sigma <= self.TAU_VAR:
            self.mem.state = "RISKY"


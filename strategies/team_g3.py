import math
import random
from collections import deque
from typing import Deque

from shared.types import MatchResult, Observation

class G3:
    """
    Implementation of Group 3's strategy: Probabilistic Tit-for-Tat.
    """
    name = "G3_ProbTFT"

    def __init__(self, history_len: int = 10, sigma: float = 1.5) -> None:
        """
        Args:
            history_len (int): Size of the sliding window (n).
            sigma (float): Standard deviation for the Gaussian distribution.
                           Controls exploration vs imitation.
        """
        self.N = 0
        self.n = history_len
        self.sigma = sigma
        # Sliding window for observations
        self.history: Deque[int] = deque(maxlen=self.n)

    def reset(self, *, N: int) -> None:
        """
        Resets the strategy for a new match.
        """
        self.N = N
        self.history.clear()

    def act(self, obs: Observation) -> int:
        """
        Decides the bid for the current round.
        """
        # 1. Calculate estimated opponent tendency (mu)
        if len(self.history) == 0:
            # Initial estimate: median of action set
            mu = (self.N + 1) / 2
        else:
            # Empirical mean of history
            mu = sum(self.history) / len(self.history)

        # 2. Calculate weights and total weight for normalization
        # Formula: w(i) = exp( - (i - mu)^2 / (2 * sigma^2) )
        weights = []
        total_weight = 0.0
        
        for i in range(1, self.N + 1):
            w = math.exp(-((i - mu) ** 2) / (2 * self.sigma ** 2))
            weights.append(w)
            total_weight += w

        # 3. Sample from the distribution (Cumulative Probability)
        u = random.random() # Uniform(0, 1)
        current_sum = 0.0
        
        for i in range(1, self.N + 1):
            # Normalized probability f(i) = w(i) / total_weight
            prob = weights[i-1] / total_weight
            current_sum += prob
            
            # Choose smallest i such that sum >= u
            if current_sum >= u:
                return i
        
        return self.N # Fallback (should not be reached due to float precision)

    def on_result(self, result: MatchResult) -> None:
        """
        Updates the history based on the round result.
        """
        # According to the spec, we observe a "censored" value.
        # If opponent acts first (opp < self): observe opponent's action.
        # Otherwise (we act first or tie): observe our own action.
        
        i_r = result.self_action
        j_r = result.opp_action

        if j_r < i_r:
            o_r = j_r
        else:
            o_r = i_r

        # Append observation to sliding window (auto-removes oldest if full)
        self.history.append(o_r)
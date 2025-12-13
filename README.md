# CAS Assignment 4

## Project Structure

```
.
├── shared/                 # Game engine (DO NOT MODIFY)
│   ├── game.py             # Payoff rules
│   ├── types.py            # Observation & MatchResult
│   ├── strategy_base.py    # Strategy interface
│   └── match.py            # 1v1 match runner
│
├── strategies/             # Team strategies
│   └── randome_bidy.py     # Simple sample strategy
│
└── run_match.py            # Entry point

```

## How to Run a Match

Edit `run_match.py` and choose the strategies you want:

```python
from shared.match import IteratedMatch, MatchConfig
from strategies.random_bid import RandomBid
from strategies.team_g2 import G2

cfg = MatchConfig(N=5, rounds=10, verbose=True)
A = RandomBid()
B = G2()

IteratedMatch(A, B, cfg).run()
```

Then run:

```bash
python run_match.py
```
or
```bash
python3 run_match.py
```

## Strategy Interface (What You Must Implement)

Every strategy must implement three methods:

```python
class Strategy:
    name: str

    def reset(self, *, N: int) -> None:
        pass

    def act(self, obs: Observation) -> int:
        pass

    def on_result(self, result: MatchResult) -> None:
        pass
```

### Method Descriptions

- `reset(N)`
  Called once before the match starts.
  Initialize memory or learning variables here.

- `act(obs)`
  Called every round.
  Must return an integer bid between `1` and `N`.

- `on_result(result)`
  Called after each round.
  Use this to update memory or learning logic.

### Observation Object

In `act(obs)`, you receive:

- `obs.N` – number of possible bids

- `obs.t` – current round number

- `obs.opp_action_history` – opponent’s past bids

- `obs.self_action_history` – your past bids

You may use as much or as little history as you want.

## Simple Example Strategy

```python
# Random strategy: chooses a random bid every round

import random
from shared.types import Observation, MatchResult

class RandomBid:
    name = "RandomBid"

    def reset(self, *, N: int) -> None:
        self.N = N

    def act(self, obs: Observation) -> int:
        return random.randint(1, self.N)

    def on_result(self, result: MatchResult) -> None:
        pass
```

## Important Rules

❌ Do NOT modify files in `shared/`

✅ Only implement your strategy file

✅ Always return a valid bid `1..N`

❌ Do NOT print inside your strategy (use `verbose=True` instead)

## Output

If `verbose=True`, each round is printed:

```
Round  1 | G2: bid=2, payoff=2, total=2 || G8: bid=4, payoff=0, total=0
Round  2 | G2: bid=1, payoff=1, total=3 || G8: bid=3, payoff=0, total=0
...
```

Final scores are shown at the end.

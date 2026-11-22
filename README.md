# Micro Chess Engine

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/nmlyz/micro-chess-engine/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/nmlyz/micro-chess-engine/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in a single Python file of under 4 KB. It plays a full game
through the match server: it reads the position, searches, and answers with
a move in UCI notation.

## How it plays

- Negamax search with alpha-beta pruning and iterative deepening to a fixed
  node budget of 40,000, so the same position always gets the same move
- No quiescence search, transposition table, killer moves, or history
  heuristic (left out to fit the 4 KB limit); move ordering is MVV-LVA only
- Evaluation from material values plus a small formula-based positional
  bonus (pawn advance and centralisation), with a bonus for the bishop pair
- En passant is not implemented (also a size trade-off); all other legal
  moves are supported

## Running it

The engine talks to a match server over HTTP. Point it at the server and
run it:

```
MAKEFUN_ENV_URL=http://localhost:8080 python3 main.py
```

It plays one game after another until the server reports the match done.
Python 3.13 and the standard library only; no other files, no network
besides the match server.

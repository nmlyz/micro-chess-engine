# Micro Chess Engine

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/nmlyz/micro-chess-engine/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/nmlyz/micro-chess-engine/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in a single Python file of under 4 KB. It plays a full game
through the match server: it reads the position, searches, and answers with
a move in UCI notation.

## How it plays

- 0x88 board with full rules: castling, en passant, promotion, check,
  checkmate, stalemate and threefold repetition
- Negamax search with alpha-beta pruning, principal variation search and
  iterative deepening, bounded by a node budget of 120,000 and a per-move
  time cap, so a move is always returned well inside the match time limit
- Quiescence search, a Zobrist-keyed transposition table, killer moves and
  a history heuristic for move ordering, plus null-move pruning and late
  move reductions
- Evaluation from material values plus piece-square tables, with a bonus
  for the bishop pair
- `main.py` is the engine packed with the kit's LZMA compressor to fit
  the 4,096-byte limit; it unpacks itself at startup and runs as plain
  Python from there

## Running it

The engine talks to a match server over HTTP. Point it at the server and
run it:

```
MAKEFUN_ENV_URL=http://localhost:8080 python3 main.py
```

It plays one game after another until the server reports the match done.
Python 3.13 and the standard library only; no other files, no network
besides the match server.

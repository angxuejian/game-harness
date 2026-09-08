# game-harness
A survival game built for LLMs to play, not humans.

```md

              state.alive = True
                     │
                START DAY
                     │
                   EVENT
                     │
             ┌───────┴───────┐
           alive           dead
             │                │
          ACTION              │
             │                │
          ACTION              │
             │                │
          ACTION              │
             │                │
          END DAY             │
             │                │
        next while            │
             │                │
             └───────┬────────┘
                     ↓
              state.alive?
                │        │
               Yes       No
                │        │
             next day    │
                         ↓
                    GAME OVER

```
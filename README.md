# game-harness
A survival game built for LLMs to play, not humans. The gameplay is based on *60 Seconds*.

## Game Rules

1. No perfect ending. Just survive as long as you can.
2. At the start of the game, the player picks 5 items from 10 items.
3. HP: 100, Stamina: 100.
4. Every day, the player loses HP from hunger and thirst.
5. Every day, the player has 3 actions. Each action costs stamina.
6. Every day, there is a random event.
7. The player has 10 bag slots. 5 are for items, and 5 are for food and water.

## Chit-chat

When I truly understood how a `harness` works, I was amazed. What a brilliant idea!

In a broad sense, we all live in a world full of `harnesses`. When we drive, we follow traffic rules. When we live in a country, we follow its laws. When we play a game, we follow the game rules. Maybe they are all different kinds of `harnesses`.

When I realized that `game-harness` is a game for LLMs, I suddenly thought of games from anime, like *Sword Art Online* and *The Legend of Luo Xiaohei: The Gate of All Living Beings*.

When the player is a human, the game needs a good user experience. The graphics can become more and more beautiful, but we still cannot build something like `Link Start`.

But LLMs are different.

For LLMs, graphics are not that important. Tokens are enough. They can make decisions, fight enemies, use items, and work with other LLMs.

The UI can simply show their decisions, battles, and logs.

Imagine several LLMs working together, fighting their way through *100 floors*, or earning the *Elfin King Folan's admiration*.

Isn't that another kind of show?



<!-- 


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

``` -->
# Twenty Fourty All

Game jam theme: Alone against all

## Game idea:

A 2048 game where you can only move one tile. This tile can push tiles
if there's room to move/merge, or pull a tile towards it. 
The goal is, as always, 2048.

A seal gyu-ing or neck extending

Arrow keys/wasd to move, click/right click to push

### Old ideas

2048 tower defense, merge tiles to get better towers (not one or all enough)

## Parts

### Grid

Is: 5x5 (6x6?) grid that the player moves around on

### Yo-chan (player), main tile

Is: The player, the "main tile"

Can:
 - Move around the grid one space at a time (WASD/Arrows/HJKL)
 - Pull an ice block towards her with a gyu (clicking)
 - Push an ice block away from her with a nobite (right clicking)

### Ice block

Is: The main "tile"

Can: 
 - Slide around the grid in the direction it's moving
 - When it hits a block of the same number, it merges into it

### Tsuki-chan

Is: An "enemy" in the game

Can:
 - Steal and a tile on the edge of the board.

### Trainer

Can:
 - Throw fish onto the grid

### Marine mammal rescue shoutout

#### Stretch goals:

 - [ ] Fish animation
 - [ ] Interactive tutorial
 - [ ] Art & Animation of the trainer
 - [ ] Art & Animation for each of the tile types
 - [ ] Animatino on tile merge
 - [ ] Trainer "gloves" (mouse cursor) as prize for beating the game
 - [ ] Add kroshik and shlissik as a more difficult enemy
 - [ ] Add Tsuki growing up and getting faster/better

## Timeline

### Actual timeline

 - [x] June 1: ideate, setup ide for python and pygame
 - [x] June 2: yo-chan grid movement working, ice block movement, nobite
 - [x] June 3: revamped ice block movement
 - [x] June 4: ice block merging, gyu, tsuki, trainer, timer, scoring
 - [x] June 5: Figured out animation, background art, board art, fish art
 - [x] June 6: Yo chan art & Tsuki art & Menu & Web build
 - [x] June 7: Sound effects, Submission
 - [ ] June 8: Church lol

### Goal

 - June 1: ideate, setup pygame
 - June 2: yo-chan grid movement working
 - June 3: ice block movement & merging
 - June 4: trainer & gyu/nobite & Tsuki
 - June 5: yo-chan art & animation system (sprites)
 - June 6: tsuki-chan art/animation & fish art/animation
 - June 7: Music & Sound Effects & Menu 
 - June 8: Packaging & Submission

## Reflections:

It was a fun process, but very draining! I'm writing this on June 7th and the
game is at a state where I think I'm ready to submit it. For my broader goal
of creating 2048 inspired games, I have made a tremendous accomplishment. This
game has complete and in tact, a board, tiles, merging, and the logic to plan
and dispatch moves. Incredibly useful. Would jam again!

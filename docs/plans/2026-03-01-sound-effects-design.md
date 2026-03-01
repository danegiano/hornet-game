# Sound Effects Design

## Overview

Add sound effects and background music to the hornet platformer. Sounds are generated programmatically using Python's built-in `wave` and `struct` modules, saved as `.wav` files, and loaded by Pygame.

**Style:** Realistic-ish — tones, impacts, and buzzing created from sine waves, square waves, and noise.

## Sound Effects

| Sound | Trigger | Generation method |
|---|---|---|
| jump | Player jumps | Rising sine sweep |
| hover | Player hovers | Low square wave buzz |
| attack | Player presses Z/X | Short noise burst + tone |
| hit_enemy | Attack hits enemy | Short thwack (noise + low tone) |
| player_hurt | Player takes damage | Low descending tone |
| enemy_die | Enemy killed | Quick pop (short noise) |
| boss_charge | Wasp King charges | Deep rumbling buzz |
| boss_slam | Wasp King slams | Heavy low impact boom |
| boss_die | Wasp King defeated | Long descending tone |
| level_complete | Level finished | Rising chime (multiple tones) |

## Music

| Track | Where | Method |
|---|---|---|
| level_music | All 3 levels | Looping melody from repeating notes |
| boss_music | Boss fight | Faster, more intense loop |

## File Structure

```
assets/sounds/       <- all .wav files
generate_sounds.py   <- script to create the .wav files
```

## Technical Approach

- `generate_sounds.py`: standalone script using `wave` + `struct` + `math` to create all `.wav` files
- `main.py`: `pygame.mixer.init()` at startup, load sounds into a dict, play at trigger points
- Sound effects volume: 50%
- Music volume: 30%
- Music loops with `pygame.mixer.music.play(-1)`
- Hover sound loops while hovering, stops when landing

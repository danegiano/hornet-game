# Asset Improvements Design — Approach B
**Date:** 2026-03-02
**Scope:** Polish + New Frames (sprites and code, no manual drawing)

## Background

All sprites are generated programmatically by Python + Pygame scripts in `tools/`.
This design describes improvements to those generator scripts plus small code changes
in `src/entities/player.py` and `src/entities/enemies.py`.

## Audit Summary

| Asset | Issue Found |
|---|---|
| `hornet_idle_0/1` | Breath bob only 1px — nearly invisible |
| `hornet_run_0/1` | Body barely leans — animation looks stiff |
| `hornet_attack_0` | Looks almost identical to idle — player can't tell they're attacking |
| Jump state | No sprite — game reuses idle while airborne |
| Damage state | No visual feedback when player is hit |
| All enemies | Only 2 frames, no attack pose |
| `bg_garden_1/2` | Transparent sky → white patches visible during parallax |

---

## Section 1: Hornet Sprite Improvements

**File:** `tools/redesign_hornet.py` (update existing)

### Idle
- Increase breath bob from 1px to 2px so the animation reads clearly at game scale
- Cloak should visibly sway between frames (widen left vs right edge)

### Run
- Lean entire body forward by tilting cloak + head position
- Cloak trails behind with a more aggressive angle
- Needle angles backward (opposite direction of travel)

### Attack
- Full lunge: body tilts ~45° forward
- Needle shoots all the way to the right edge of the 32×32 frame
- Add a white slash arc `pygame.draw.arc` around the needle tip
- Body shadow is suppressed to sell the forward momentum

### New: `hornet_jump.png`
- Wings spread wide (large semi-transparent ellipses on both sides)
- Body tucked slightly upward (head higher, cloak shorter)
- Needle points downward

### New: `hornet_hurt.png`
- Same shape as `hornet_idle_0` but entire surface tinted bright white
- Achieved by drawing the normal sprite then blitting a white overlay with `BLEND_ADD`

---

## Section 2: Player Code Changes

**File:** `src/entities/player.py`

### Load new sprites
- Load `hornet_jump.png` and its flip at startup (same scale pipeline as existing sprites)
- Load `hornet_hurt.png` and its flip

### Hurt flash system
- Add `self.hurt_flash_timer = 0` to `__init__`
- In `take_damage()`: when damage is actually applied, set `self.hurt_flash_timer = 12`
- Each frame: decrement `hurt_flash_timer` if > 0
- In `draw()`: if `hurt_flash_timer > 0` and frame is even (blink), substitute hurt sprite

### Jump animation state
- Add `"jump"` to the anim_mode logic: when `not self.on_ground` and not attacking, use `"jump"`
- Jump sprite does not cycle frames (single frame)

---

## Section 3: Enemy Attack Frames

**File:** `tools/make_mobs.py` (update existing)

### Wasp (yellow + red)
- Frame 2: body angled forward like a dart, stinger fully thrust out to edge of frame
- Applied to both `wasp_yellow` and `wasp_red` variants

### Spider
- Frame 2: front two legs reared up high, abdomen lowered, fangs dots more visible

### Fly
- Frame 2: wings swept back flat, body angled downward into a dive

**File:** `src/entities/enemies.py`

- Add `self.hurt_flash_timer = 0` to Enemy base `__init__`
- When enemy takes damage: `self.hurt_flash_timer = 8`
- Each frame: decrement `hurt_flash_timer`
- In enemy draw: if `hurt_flash_timer > 0` and even frame, blit white overlay over sprite
- Enemies use their attack frame (index 2) when within 60px of player on x-axis

---

## Section 4: Garden Background Fix

**File:** `tools/make_bg.py`

- Layer 1 (`bg_garden_1.png`): fill surface with sky gradient `(135, 180, 220)` before drawing mountains
- Layer 2 (`bg_garden_2.png`): fill with slightly lighter blue `(160, 200, 230)` before drawing trees
- Layer 3 (`bg_garden_3.png`): already solid (bushes fill the bottom), no change needed

---

## Section 5: Enemy Death Burst (Code Only)

**File:** `src/entities/enemies.py` and `src/game.py`

- On enemy death, emit 5–6 `Particle` objects with:
  - Random direction (spread 360°)
  - Color matching the enemy type (yellow for wasp, brown for spider, dark for fly)
  - Lifetime: 20 frames, fade out linearly
  - Size: 3px circle, shrinks to 1px at end
- Particles stored in `game.particles` list, drawn in `game.draw()`, updated in `game.update()`

---

## Files Changed

| File | Type of change |
|---|---|
| `tools/redesign_hornet.py` | Update generator — better animations + 2 new sprites |
| `tools/make_mobs.py` | Update generator — add attack frame per enemy |
| `tools/make_bg.py` | Update generator — fix garden sky |
| `src/entities/player.py` | Load new sprites, add hurt flash, add jump anim state |
| `src/entities/enemies.py` | Add hurt flash, attack frame, death particle emit |
| `src/game.py` | Add particle list, update + draw particles |

---

## Success Criteria

- [ ] Hornet attack animation is visually obvious — player clearly sees a lunge
- [ ] Hornet jump sprite shows while airborne
- [ ] Player flashes white briefly when taking damage
- [ ] Each enemy has a visible attack pose when close to the player
- [ ] Enemies flash white when hit
- [ ] Colored particles burst from enemies on death
- [ ] Garden parallax has no white/transparent sky patches

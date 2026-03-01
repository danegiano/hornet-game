# Sound Effects Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add programmatically generated sound effects and background music to the hornet platformer.

**Architecture:** A standalone `generate_sounds.py` script creates all `.wav` files using Python's built-in `wave` and `struct` modules. The `main.py` loads these files via `pygame.mixer` and plays them at the appropriate moments. Sound generation is a one-time setup step.

**Tech Stack:** Python 3 (wave, struct, math, random), Pygame mixer

---

### Task 1: Create the Sound Generator Script

**Files:**
- Create: `generate_sounds.py`

**Step 1: Create generate_sounds.py with helper functions and all sound effects**

This script generates all 12 `.wav` files. It uses:
- Sine waves for tones (jump, level_complete, boss_die)
- Square waves for buzzy sounds (hover, boss_charge)
- Noise for impacts (attack, hit_enemy, slam)
- Mixed waveforms for complex sounds

```python
import wave
import struct
import math
import random
import os

SAMPLE_RATE = 44100

def save_wav(filename, samples, sample_rate=SAMPLE_RATE):
    """Save a list of float samples (-1.0 to 1.0) as a .wav file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)  # 16-bit
        f.setframerate(sample_rate)
        for s in samples:
            # Clamp to [-1, 1] and convert to 16-bit int
            s = max(-1.0, min(1.0, s))
            f.writeframes(struct.pack('<h', int(s * 32767)))

def sine_wave(freq, duration, volume=0.5):
    """Generate a sine wave tone."""
    samples = []
    num_samples = int(SAMPLE_RATE * duration)
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        samples.append(volume * math.sin(2 * math.pi * freq * t))
    return samples

def square_wave(freq, duration, volume=0.3):
    """Generate a buzzy square wave."""
    samples = []
    num_samples = int(SAMPLE_RATE * duration)
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        val = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
        samples.append(volume * val)
    return samples

def noise(duration, volume=0.3):
    """Generate white noise."""
    samples = []
    num_samples = int(SAMPLE_RATE * duration)
    for i in range(num_samples):
        samples.append(volume * (random.random() * 2 - 1))
    return samples

def fade_out(samples):
    """Apply a fade-out envelope to samples."""
    length = len(samples)
    for i in range(length):
        samples[i] *= 1.0 - (i / length)
    return samples

def fade_in_out(samples, fade_fraction=0.1):
    """Apply fade-in and fade-out."""
    length = len(samples)
    fade_len = int(length * fade_fraction)
    for i in range(fade_len):
        samples[i] *= i / fade_len
    for i in range(fade_len):
        samples[length - 1 - i] *= i / fade_len
    return samples

def mix(samples_a, samples_b):
    """Mix two sample lists together (same length)."""
    length = min(len(samples_a), len(samples_b))
    return [samples_a[i] + samples_b[i] for i in range(length)]

def sweep(freq_start, freq_end, duration, volume=0.5):
    """Sine wave that sweeps from one frequency to another."""
    samples = []
    num_samples = int(SAMPLE_RATE * duration)
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        freq = freq_start + (freq_end - freq_start) * progress
        samples.append(volume * math.sin(2 * math.pi * freq * t))
    return samples

def generate_all():
    sound_dir = os.path.join("assets", "sounds")

    # Jump — quick rising buzz
    s = sweep(200, 600, 0.15, 0.4)
    s = fade_out(s)
    save_wav(os.path.join(sound_dir, "jump.wav"), s)
    print("  jump.wav")

    # Hover — low buzzy loop (longer for looping)
    s = square_wave(120, 0.5, 0.15)
    s = fade_in_out(s)
    save_wav(os.path.join(sound_dir, "hover.wav"), s)
    print("  hover.wav")

    # Attack — sharp swoosh
    s = noise(0.08, 0.4)
    tone = sweep(800, 200, 0.08, 0.3)
    s = mix(s, tone)
    s = fade_out(s)
    save_wav(os.path.join(sound_dir, "attack.wav"), s)
    print("  attack.wav")

    # Hit enemy — thwack
    s = noise(0.05, 0.5)
    tone = sine_wave(300, 0.05, 0.4)
    s = mix(s, tone)
    s = fade_out(s)
    save_wav(os.path.join(sound_dir, "hit_enemy.wav"), s)
    print("  hit_enemy.wav")

    # Player hurt — low descending tone
    s = sweep(400, 150, 0.3, 0.4)
    s = fade_out(s)
    save_wav(os.path.join(sound_dir, "player_hurt.wav"), s)
    print("  player_hurt.wav")

    # Enemy die — quick pop
    s = noise(0.03, 0.4)
    tone = sweep(600, 100, 0.1, 0.3)
    s2 = fade_out(tone)
    # Pad noise to match tone length
    s = s + [0.0] * (len(s2) - len(s))
    s = mix(s, s2)
    save_wav(os.path.join(sound_dir, "enemy_die.wav"), s)
    print("  enemy_die.wav")

    # Boss charge — deep rumble
    s = square_wave(60, 0.4, 0.25)
    n = noise(0.4, 0.15)
    s = mix(s, n)
    s = fade_in_out(s, 0.2)
    save_wav(os.path.join(sound_dir, "boss_charge.wav"), s)
    print("  boss_charge.wav")

    # Boss slam — heavy impact
    s = noise(0.1, 0.6)
    tone = sweep(150, 40, 0.3, 0.5)
    # Pad noise to match tone length
    s = s + [0.0] * (len(tone) - len(s))
    s = mix(s, tone)
    s = fade_out(s)
    save_wav(os.path.join(sound_dir, "boss_slam.wav"), s)
    print("  boss_slam.wav")

    # Boss die — long descending tone
    s = sweep(500, 60, 1.0, 0.4)
    s2 = sweep(750, 90, 1.0, 0.2)
    s = mix(s, s2)
    s = fade_out(s)
    save_wav(os.path.join(sound_dir, "boss_die.wav"), s)
    print("  boss_die.wav")

    # Level complete — rising chime (three quick ascending notes)
    note1 = fade_out(sine_wave(523, 0.15, 0.4))  # C5
    note2 = fade_out(sine_wave(659, 0.15, 0.4))  # E5
    note3 = fade_out(sine_wave(784, 0.3, 0.4))   # G5
    gap = [0.0] * int(SAMPLE_RATE * 0.05)
    s = note1 + gap + note2 + gap + note3
    save_wav(os.path.join(sound_dir, "level_complete.wav"), s)
    print("  level_complete.wav")

    # Level music — simple looping melody
    # Notes: C4, E4, G4, A4 pattern repeated, with a bass drone
    notes = [262, 330, 392, 440, 392, 330, 262, 330]
    note_dur = 0.25
    melody = []
    for freq in notes:
        note = sine_wave(freq, note_dur, 0.2)
        note = fade_in_out(note, 0.05)
        melody.extend(note)
    # Repeat 4 times for a longer loop
    melody = melody * 4
    # Add a bass drone underneath
    bass = square_wave(65, len(melody) / SAMPLE_RATE, 0.08)
    melody = mix(melody, bass)
    save_wav(os.path.join(sound_dir, "level_music.wav"), melody)
    print("  level_music.wav")

    # Boss music — faster, more intense
    notes = [330, 330, 392, 330, 294, 330, 392, 440]
    note_dur = 0.18
    melody = []
    for freq in notes:
        note = square_wave(freq, note_dur, 0.15)
        note = fade_in_out(note, 0.05)
        melody.extend(note)
    melody = melody * 4
    bass = square_wave(82, len(melody) / SAMPLE_RATE, 0.1)
    melody = mix(melody, bass)
    save_wav(os.path.join(sound_dir, "boss_music.wav"), melody)
    print("  boss_music.wav")

    print("\nAll sounds generated!")

if __name__ == "__main__":
    print("Generating sound effects...")
    generate_all()
```

**Step 2: Run the generator to create all sound files**

Run: `python generate_sounds.py`
Expected: Creates `assets/sounds/` with 12 `.wav` files.

**Step 3: Commit**

```bash
git add generate_sounds.py assets/sounds/
git commit -m "feat: add sound generator script and generated .wav files"
```

---

### Task 2: Load Sounds in main.py

**Files:**
- Modify: `main.py`

**Step 1: Initialize pygame.mixer and load sounds**

In `main()`, right after `pygame.init()` (line 816), add mixer init and sound loading:

```python
    pygame.mixer.init()

    # Load sound effects
    sound_dir = os.path.join("assets", "sounds")
    sounds = {}
    sound_names = [
        "jump", "hover", "attack", "hit_enemy", "player_hurt",
        "enemy_die", "boss_charge", "boss_slam", "boss_die", "level_complete"
    ]
    for name in sound_names:
        path = os.path.join(sound_dir, f"{name}.wav")
        if os.path.exists(path):
            sounds[name] = pygame.mixer.Sound(path)
            sounds[name].set_volume(0.5)
    # Hover sound needs to loop, set it quieter
    if "hover" in sounds:
        sounds["hover"].set_volume(0.3)
```

**Step 2: Add a helper to play music**

After the sound loading block:

```python
    def play_music(track_name):
        """Load and play background music on loop."""
        path = os.path.join(sound_dir, f"{track_name}.wav")
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # -1 = loop forever

    def stop_music():
        pygame.mixer.music.stop()
```

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: load sound effects and music in main.py"
```

---

### Task 3: Add Sound Triggers — Player Actions

**Files:**
- Modify: `main.py`

**Step 1: Play jump sound**

In the event loop, when jumping is detected — but since jump is in `Player.update()` via `keys`, we need a different approach. Add a `jumped` flag:

After the player update call (around line 868), detect if player just jumped:
```python
            # Detect jump (player was on ground, now isn't, and vel_y is negative)
            old_on_ground = player.on_ground
```

Actually, simpler approach: modify Player to track if it just jumped this frame.

In Player.__init__, add:
```python
        self.just_jumped = False
```

In Player.update(), in the jump section (around line 142), set the flag:
```python
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False
            self.just_jumped = True
        else:
            self.just_jumped = False
```

Then in main() game loop, after `player.update(keys, platforms)`:
```python
            if player.just_jumped and "jump" in sounds:
                sounds["jump"].play()
```

**Step 2: Play hover sound (looping)**

Track hover state to start/stop the loop. Add a variable in main():
```python
    hover_channel = None
```

In the game loop, after player update:
```python
            # Hover sound — start loop when hovering begins, stop when it ends
            if player.is_hovering and "hover" in sounds:
                if hover_channel is None or not hover_channel.get_busy():
                    hover_channel = sounds["hover"].play(-1)  # -1 = loop
            else:
                if hover_channel and hover_channel.get_busy():
                    hover_channel.stop()
                    hover_channel = None
```

**Step 3: Play attack sound**

In the event loop where attack is triggered (line 863-864):
```python
                if event.key in (pygame.K_z, pygame.K_x) and game_state == STATE_PLAYING:
                    player.start_attack()
                    if "attack" in sounds:
                        sounds["attack"].play()
```

**Step 4: Commit**

```bash
git add main.py
git commit -m "feat: add jump, hover, and attack sound effects"
```

---

### Task 4: Add Sound Triggers — Combat

**Files:**
- Modify: `main.py`

**Step 1: Make handle_combat return events**

Change `handle_combat` to return a list of sound event strings so main() knows what happened:

```python
def handle_combat(player, enemies, boss=None):
    hit_events = []

    # Player attack hits enemies
    if player.attacking and player.attack_rect:
        for enemy in enemies:
            if enemy.alive and player.attack_rect.colliderect(enemy.rect):
                enemy.take_damage(1)
                if not enemy.alive:
                    hit_events.append("enemy_die")
                else:
                    hit_events.append("hit_enemy")
        # Player attack hits boss
        if boss and boss.alive and player.attack_rect.colliderect(boss.rect):
            boss.take_damage(1)
            if not boss.alive:
                hit_events.append("boss_die")
            else:
                hit_events.append("hit_enemy")

    # Enemies damage player on contact
    for enemy in enemies:
        if enemy.alive and player.rect.colliderect(enemy.rect):
            if player.take_damage(1):
                if player.rect.centerx < enemy.rect.centerx:
                    player.rect.x -= 30
                else:
                    player.rect.x += 30
                player.vel_y = -8
                hit_events.append("player_hurt")

    # Boss damages player
    if boss and boss.alive:
        if player.rect.colliderect(boss.rect):
            if player.take_damage(1):
                if player.rect.centerx < boss.rect.centerx:
                    player.rect.x -= 40
                else:
                    player.rect.x += 40
                player.vel_y = -10
                hit_events.append("player_hurt")
        if boss.shockwave and boss.shockwave_timer > 0:
            if player.rect.colliderect(boss.shockwave):
                if player.take_damage(1):
                    player.vel_y = -12
                    hit_events.append("player_hurt")

    return hit_events
```

**Step 2: Play combat sounds in main()**

Where handle_combat is called (line 880), capture events and play sounds:

```python
            combat_events = handle_combat(player, enemies, boss)
            for event in combat_events:
                if event in sounds:
                    sounds[event].play()
```

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add combat sound effects (hit, kill, hurt)"
```

---

### Task 5: Add Sound Triggers — Boss & Level Events

**Files:**
- Modify: `main.py`

**Step 1: Add boss attack sounds**

Track boss state changes. In the game loop boss update section, detect when boss starts an attack:

Add a variable before the game loop:
```python
    prev_boss_state = "idle"
```

After `boss.update(player, platforms)`:
```python
                if boss.state != prev_boss_state:
                    if boss.state == "charge" and "boss_charge" in sounds:
                        sounds["boss_charge"].play()
                    elif boss.state == "slam" and "boss_slam" in sounds:
                        sounds["boss_slam"].play()
                    prev_boss_state = boss.state
```

Reset `prev_boss_state` in start_level:
```python
        prev_boss_state = "idle"
```

**Step 2: Add music triggers**

When game state changes to STATE_PLAYING, start level music:
- In the STATE_TITLE -> STATE_PLAYING transition: `play_music("level_music")`
- In the STATE_GAME_OVER -> STATE_PLAYING transition: `play_music("level_music")`
- In the STATE_LEVEL_TRANSITION -> STATE_PLAYING transition: `play_music("level_music")`
- When boss spawns (current_level == 2 and player reaches boss area): switch to `play_music("boss_music")`
- On game over: `stop_music()`
- On victory: `stop_music()`

For boss music, add a flag `boss_music_started = False` and check in the game loop:
```python
            if boss and boss.alive and not boss_music_started:
                # Start boss music when player reaches the arena
                if player.rect.x > 1700:
                    play_music("boss_music")
                    boss_music_started = True
```

**Step 3: Play level complete sound**

When level completion is detected:
```python
            elif current_level < 2 and check_level_complete(player, enemies):
                current_level += 1
                game_state = STATE_LEVEL_TRANSITION
                stop_music()
                if "level_complete" in sounds:
                    sounds["level_complete"].play()
```

**Step 4: Stop hover sound on state changes**

When game state changes away from playing (death, level complete):
```python
                if hover_channel and hover_channel.get_busy():
                    hover_channel.stop()
                    hover_channel = None
```

**Step 5: Commit**

```bash
git add main.py
git commit -m "feat: add boss sounds, music, and level complete jingle"
```

---

### Task 6: Final Verification

**Files:**
- None (testing only)

**Step 1: Run generate_sounds.py to ensure all files exist**

Run: `python generate_sounds.py`
Expected: All 12 .wav files generated in assets/sounds/

**Step 2: Run the game and test all sounds**

Run: `python main.py`

Test checklist:
- [ ] Title screen: no music (silence)
- [ ] Start game: level music plays
- [ ] Jump: rising buzz sound
- [ ] Hover: buzzing loop while holding space in air, stops on landing
- [ ] Attack (Z/X): sharp swoosh
- [ ] Hit enemy: thwack sound
- [ ] Kill enemy: pop sound
- [ ] Get hit by enemy: low descending hurt sound
- [ ] Complete level: music stops, chime plays
- [ ] Level transition -> next level: music restarts
- [ ] Reach boss arena in level 3: music switches to boss music
- [ ] Hit boss: thwack sound
- [ ] Boss charges: deep rumble
- [ ] Boss slams: heavy impact
- [ ] Defeat boss: long descending tone, music stops
- [ ] Game over: music stops
- [ ] Victory screen: no music

**Step 3: Final commit and push**

```bash
git push
```

---

## Summary

| Task | What it adds | Depends on |
|------|-------------|------------|
| 1 | Sound generator script + .wav files | — |
| 2 | Sound loading in main.py | 1 |
| 3 | Player sounds (jump, hover, attack) | 2 |
| 4 | Combat sounds (hit, kill, hurt) | 2 |
| 5 | Boss sounds + music + level complete | 3, 4 |
| 6 | Final verification | 5 |

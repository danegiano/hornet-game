"""
generate_sounds.py — Creates all .wav sound files for Hornet game.
Uses only Python built-in modules: wave, struct, math, random, os.
No pip installs needed!

Run with: python generate_sounds.py
Output:   assets/sounds/*.wav (12 files)
"""

import wave
import struct
import math
import random
import os

# Audio settings — 44100 samples per second, mono (1 channel), 16-bit
SAMPLE_RATE = 44100

# ─────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

def save_wav(filename, samples):
    """
    Save a list of float samples (-1.0 to 1.0) as a 16-bit mono .wav file.
    'filename' should be a full path like 'assets/sounds/jump.wav'.
    """
    # Make sure the folder exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Clamp samples to the safe range [-1.0, 1.0]
    clamped = [max(-1.0, min(1.0, s)) for s in samples]

    # Convert floats to 16-bit signed integers (-32768 to 32767)
    int_samples = [int(s * 32767) for s in clamped]

    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)           # Mono
        wf.setsampwidth(2)           # 2 bytes = 16-bit
        wf.setframerate(SAMPLE_RATE) # 44100 Hz
        # Pack each integer into a 16-bit little-endian binary value
        data = struct.pack('<' + 'h' * len(int_samples), *int_samples)
        wf.writeframes(data)

    print(f"  Saved: {filename}  ({len(samples)} samples, {len(samples)/SAMPLE_RATE:.3f}s)")


def sine_wave(freq, duration, volume=0.5):
    """
    Generate a pure sine wave.
    freq     — pitch in Hz (e.g. 440 = concert A)
    duration — length in seconds
    volume   — 0.0 (silent) to 1.0 (full)
    Returns a list of float samples.
    """
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        value = math.sin(2 * math.pi * freq * t) * volume
        samples.append(value)
    return samples


def square_wave(freq, duration, volume=0.5):
    """
    Generate a square wave — sounds buzzy and retro.
    Works the same as sine_wave but snaps to +volume or -volume.
    """
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # math.sin is positive in the first half of each cycle, negative in the second
        value = volume if math.sin(2 * math.pi * freq * t) >= 0 else -volume
        samples.append(value)
    return samples


def noise(duration, volume=0.5):
    """
    Generate white noise — random static, good for impacts and explosions.
    """
    num_samples = int(SAMPLE_RATE * duration)
    return [random.uniform(-volume, volume) for _ in range(num_samples)]


def sweep(freq_start, freq_end, duration, volume=0.5):
    """
    Sine sweep — slides from one frequency to another over 'duration' seconds.
    Great for whooshes, rising/falling sounds, and laser effects.
    """
    num_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Linearly interpolate the frequency at this moment in time
        progress = t / duration
        freq = freq_start + (freq_end - freq_start) * progress
        value = math.sin(2 * math.pi * freq * t) * volume
        samples.append(value)
    return samples


def fade_out(samples):
    """
    Apply a linear fade-out to a sample list.
    The sound starts at full volume and drops to silence at the end.
    Returns a new list (doesn't modify the original).
    """
    n = len(samples)
    return [s * (1.0 - i / n) for i, s in enumerate(samples)]


def fade_in_out(samples, fade_fraction=0.1):
    """
    Apply fade-in at the start and fade-out at the end.
    fade_fraction — how much of the sound to use for each fade (e.g. 0.1 = 10%).
    """
    n = len(samples)
    fade_len = int(n * fade_fraction)
    result = list(samples)

    # Fade in: ramp from 0 to 1
    for i in range(fade_len):
        result[i] *= i / fade_len

    # Fade out: ramp from 1 to 0
    for i in range(fade_len):
        result[n - 1 - i] *= i / fade_len

    return result


def mix(samples_a, samples_b):
    """
    Add two sample lists together (mix two sounds).
    If one list is shorter, it's treated as zeros for the extra part.
    Returns a new list the length of the longer input.
    """
    n = max(len(samples_a), len(samples_b))
    result = []
    for i in range(n):
        a = samples_a[i] if i < len(samples_a) else 0.0
        b = samples_b[i] if i < len(samples_b) else 0.0
        result.append(a + b)
    return result


def silence(duration):
    """Helper: generate a block of zeros (silence)."""
    return [0.0] * int(SAMPLE_RATE * duration)


# ─────────────────────────────────────────────────────────────
# SOUND GENERATION
# ─────────────────────────────────────────────────────────────

def make_jump():
    """
    jump.wav — Quick rising buzz (0.15s).
    A sine sweep from 200 Hz up to 600 Hz with a fade-out.
    Sounds like a quick insect-wing flap upward.
    """
    samples = sweep(200, 600, 0.15, volume=0.6)
    samples = fade_out(samples)
    save_wav("assets/sounds/jump.wav", samples)


def make_hover():
    """
    hover.wav — Low buzz loop (0.5s).
    A square wave at 120 Hz with a fade-in and fade-out.
    Loops nicely to simulate a hovering insect sound.
    """
    samples = square_wave(120, 0.5, volume=0.3)
    samples = fade_in_out(samples, fade_fraction=0.15)
    save_wav("assets/sounds/hover.wav", samples)


def make_attack():
    """
    attack.wav — Sharp swoosh (0.08s).
    White noise mixed with a descending sweep, faded out.
    Very short and snappy — sounds like a quick strike.
    """
    n_samples = noise(0.08, volume=0.4)
    s_samples = sweep(800, 200, 0.08, volume=0.5)
    samples = mix(n_samples, s_samples)
    samples = fade_out(samples)
    save_wav("assets/sounds/attack.wav", samples)


def make_hit_enemy():
    """
    hit_enemy.wav — Thwack (0.05s).
    Noise mixed with a short sine tone, faded out.
    That satisfying "thwack" when you hit something.
    """
    n_samples = noise(0.05, volume=0.5)
    s_samples = sine_wave(300, 0.05, volume=0.4)
    samples = mix(n_samples, s_samples)
    samples = fade_out(samples)
    save_wav("assets/sounds/hit_enemy.wav", samples)


def make_player_hurt():
    """
    player_hurt.wav — Low descending tone (0.3s).
    A sweep from 400 Hz down to 150 Hz — sounds like "oof".
    """
    samples = sweep(400, 150, 0.3, volume=0.6)
    samples = fade_out(samples)
    save_wav("assets/sounds/player_hurt.wav", samples)


def make_enemy_die():
    """
    enemy_die.wav — Quick pop (0.1s).
    Noise mixed with a descending sweep from 600 to 100 Hz, faded out.
    A satisfying "pop" when an enemy is defeated.
    """
    n_samples = noise(0.1, volume=0.4)
    s_samples = sweep(600, 100, 0.1, volume=0.5)
    samples = mix(n_samples, s_samples)
    samples = fade_out(samples)
    save_wav("assets/sounds/enemy_die.wav", samples)


def make_boss_charge():
    """
    boss_charge.wav — Deep rumble (0.4s).
    A very low square wave at 60 Hz mixed with noise, with fade-in and fade-out.
    Feels like something big powering up.
    """
    sq_samples = square_wave(60, 0.4, volume=0.35)
    n_samples  = noise(0.4, volume=0.15)
    samples = mix(sq_samples, n_samples)
    samples = fade_in_out(samples, fade_fraction=0.2)
    save_wav("assets/sounds/boss_charge.wav", samples)


def make_boss_slam():
    """
    boss_slam.wav — Heavy impact (0.3s).
    Noise mixed with a deep descending sweep 150 -> 40 Hz, faded out.
    Big, heavy, ground-shaking thud.
    """
    n_samples = noise(0.3, volume=0.5)
    s_samples = sweep(150, 40, 0.3, volume=0.5)
    samples = mix(n_samples, s_samples)
    samples = fade_out(samples)
    save_wav("assets/sounds/boss_slam.wav", samples)


def make_boss_die():
    """
    boss_die.wav — Long descending sound (1.0s).
    Two overlapping sweeps to make a richer sound, both fading out.
    A dramatic, slow death sound for a big boss.
    """
    sweep1 = sweep(500, 60,  1.0, volume=0.45)
    sweep2 = sweep(750, 90,  1.0, volume=0.35)
    samples = mix(sweep1, sweep2)
    samples = fade_out(samples)
    save_wav("assets/sounds/boss_die.wav", samples)


def make_level_complete():
    """
    level_complete.wav — Rising chime.
    Three sine notes C5 (523 Hz), E5 (659 Hz), G5 (784 Hz) with short gaps.
    That classic "you did it!" ascending arpeggio.
    """
    # Musical note frequencies
    C5 = 523.25
    E5 = 659.25
    G5 = 783.99

    note_dur = 0.18   # each note is 0.18s
    gap_dur  = 0.05   # tiny silence between notes

    note_c = fade_out(sine_wave(C5, note_dur, volume=0.55))
    note_e = fade_out(sine_wave(E5, note_dur, volume=0.55))
    note_g = fade_out(sine_wave(G5, note_dur + 0.1, volume=0.55))  # last note held longer

    gap = silence(gap_dur)

    samples = note_c + gap + note_e + gap + note_g
    save_wav("assets/sounds/level_complete.wav", samples)


def make_level_music():
    """
    level_music.wav — Upbeat loop (~8s).
    A simple melody using C4, E4, G4, A4 repeated 4 times,
    with a constant square-wave bass drone underneath.
    Sounds like a cheerful little background tune.
    """
    # Note frequencies (4th octave)
    C4 = 261.63
    E4 = 329.63
    G4 = 392.00
    A4 = 440.00

    # Each note in the melody is 0.25s (quarter note at 240 BPM)
    note_dur = 0.25

    # Build one bar: C E G A G E C E
    melody_pattern = [C4, E4, G4, A4, G4, E4, C4, E4]

    one_bar = []
    for freq in melody_pattern:
        note = sine_wave(freq, note_dur, volume=0.45)
        note = fade_in_out(note, fade_fraction=0.1)
        one_bar.extend(note)

    # Repeat the bar 4 times (~8 seconds total)
    melody = one_bar * 4

    # Bass drone: square wave at C2 (65 Hz) for the whole duration
    total_dur = len(melody) / SAMPLE_RATE
    bass = square_wave(65.41, total_dur, volume=0.2)
    bass = fade_in_out(bass, fade_fraction=0.05)

    samples = mix(melody, bass)
    save_wav("assets/sounds/level_music.wav", samples)


def make_boss_music():
    """
    boss_music.wav — Intense loop (~6s).
    A driving square-wave melody on E4 with rhythmic variation,
    plus a deep square-wave bass at E2.
    Tense and relentless — boss fight energy.
    """
    E4 = 329.63
    B3 = 246.94
    D4 = 293.66

    note_dur = 0.15   # shorter notes = faster, more urgent feel

    # Melody pattern: E E E B D E
    melody_pattern = [E4, E4, E4, B3, D4, E4, D4, B3]

    one_bar = []
    for freq in melody_pattern:
        note = square_wave(freq, note_dur, volume=0.35)
        note = fade_in_out(note, fade_fraction=0.1)
        one_bar.extend(note)

    # Repeat 5 times (~6 seconds)
    melody = one_bar * 5

    # Bass drone: E2 (82 Hz) square wave
    total_dur = len(melody) / SAMPLE_RATE
    bass = square_wave(82.41, total_dur, volume=0.25)
    bass = fade_in_out(bass, fade_fraction=0.05)

    samples = mix(melody, bass)
    save_wav("assets/sounds/boss_music.wav", samples)


# ─────────────────────────────────────────────────────────────
# MAIN — run all generators
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating sound files for Hornet game...")
    print()

    make_jump()
    make_hover()
    make_attack()
    make_hit_enemy()
    make_player_hurt()
    make_enemy_die()
    make_boss_charge()
    make_boss_slam()
    make_boss_die()
    make_level_complete()
    make_level_music()
    make_boss_music()

    print()
    print("All 12 sound files created in assets/sounds/")

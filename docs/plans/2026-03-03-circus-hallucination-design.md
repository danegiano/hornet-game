# Design: The Circus + Hallucination Land
_Date: 2026-03-03_

## Summary
Two major endgame additions unlocked after beating the final boss (Shadow Hornet on Island 5).

---

## Part 1 — Achievement + Circus Unlock

- Beating Shadow Hornet triggers an **achievement popup**
- The island map gains a new location: **The Circus**
- The Circus is only visible/accessible after the achievement is earned
- Save data tracks whether the achievement is unlocked

---

## Part 2 — The Circus (Boss Rush)

**Goal:** Fight all 5 island bosses back-to-back, stronger versions.

**Rules:**
- Enter from the island map (new icon/spot)
- Bosses fight in order: Garden → Swamp → Crystal Caves → Volcano → Shadow Fortress
- Each boss is a harder version (more HP, faster, harder attack patterns)
- Player has **one life** — die once, restart from boss 1
- Beat all 5 bosses → a **portal appears**
- Going through the portal unlocks **Hallucination Land**

**Circus boss difficulty modifiers:**
- +50% HP
- +25% movement speed
- Attacks deal +1 extra damage

---

## Part 3 — Hallucination Land

**Structure:**
- 5 islands, 4 levels each (20 levels total)
- Every normal enemy is in **shadow form** + has stronger stats + better traits
- Each level has **1 boss** (4 bosses per island, 20 bosses total)
- Bosses are new hallucination versions (shadow + harder)

**Special Shop (per island):**
- Sells up to **10 lives** in stock (way more than normal)
- Sells a unique set of **shadow powers** per island
- Shadow powers are stronger than normal powers
- Shop is different for each of the 5 hallucination islands

**Shadow Powers (one set per island, 5 total sets):**
- Island 1 powers: TBD during implementation
- Island 2 powers: TBD
- Island 3 powers: TBD
- Island 4 powers: TBD
- Island 5 powers: TBD

---

## Save Data Changes
- `circus_unlocked: bool` — whether achievement has been earned
- `hallucination_unlocked: bool` — whether Hallucination Land portal has been opened
- `hallucination_island: int` — furthest hallucination island reached
- `shadow_powers: list` — shadow powers the player has unlocked

---

## Build Order

1. **The Circus first** — reuses existing boss code, self-contained, fast to implement
2. **Hallucination Land second** — new world built on top of existing level system

---

## Files Likely Affected
- `src/settings.py` — circus/hallucination constants, island data
- `src/save_data.py` — new save fields
- `src/game.py` — new game states, circus/hallucination logic
- `src/ui/island_map.py` — show Circus on map, Hallucination Land map
- `src/entities/bosses.py` — circus difficulty modifiers
- `src/world/levels.py` — hallucination level generation
- `src/ui/shop.py` — hallucination shop with shadow powers
- `src/systems/powers.py` — shadow power definitions

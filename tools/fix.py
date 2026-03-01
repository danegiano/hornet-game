import re
with open("main.py", "r") as f:
    s = f.read()

# Fix the boss = None bg = None messed up indentation
s = re.sub(r"        else:\n            boss = None\n    bg = None\n        prev_boss_state = \"idle\"", r"        else:\n            boss = None\n        prev_boss_state = \"idle\"", s)

# Fix the time_ms indent
bad_chunk = r"        elif game_state == STATE_PLAYING:\n.*time_ms = pygame\.time\.get_ticks\(\)\n\s*if bg:\n\s*bg\.draw\(screen, camera\.x\)\n\s*else:\n\s*screen\.fill\(LEVEL_THEMES\[current_level\]\[\"bg\"\]\)"
good_chunk = r"""        elif game_state == STATE_PLAYING:
            time_ms = pygame.time.get_ticks()
            if bg:
                bg.draw(screen, camera.x)
            else:
                screen.fill(LEVEL_THEMES[current_level]["bg"])"""

s = re.sub(bad_chunk, good_chunk, s)

with open("main.py", "w") as f:
    f.write(s)

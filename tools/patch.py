import os

with open("main.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("    bg = None"):
        continue
    if "prev_boss_state = \\\"idle\\\"" in line:
        line = line.replace("\\\"idle\\\"", "\"idle\"")
    if line.startswith("time_ms = pygame.time.get_ticks()"):
        line = "            time_ms = pygame.time.get_ticks()\n"
    new_lines.append(line)

with open("main.py", "w") as f:
    f.writelines(new_lines)


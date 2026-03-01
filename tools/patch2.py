with open("main.py", "r") as f:
    s = f.read()

s = s.replace("boss = None\n\n    def start_level():", "boss = None\n    bg = None\n\n    def start_level():")
s = s.replace("boss = None\n    prev_boss_state = \"idle\"", "boss = None\n    bg = None\n    prev_boss_state = \"idle\"")

with open("main.py", "w") as f:
    f.write(s)

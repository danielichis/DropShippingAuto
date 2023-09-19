import json
# leer el archivo json de amazon

with open(r"data.json", "r",encoding="utf-8") as f:
    state = json.load(f)
    print(state)

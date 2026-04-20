import json

with open("data/annotations.json") as f:
    data = json.load(f)

print("Total samples:", len(data))

for i in range(min(5, len(data))):
    print(data[i])
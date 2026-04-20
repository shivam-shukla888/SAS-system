import os, json, shutil

SOURCE = "gnhk_dataset"
DEST = "data"

os.makedirs(f"{DEST}/images", exist_ok=True)

all_annotations = []

for split in ["train", "test"]:
    split_path = os.path.join(SOURCE, split)

    for file in os.listdir(split_path):
        if file.endswith(".json"):

            json_path = os.path.join(split_path, file)
            img_path = json_path.replace(".json", ".jpg")

            if not os.path.exists(img_path):
                img_path = json_path.replace(".json", ".png")

            if not os.path.exists(img_path):
                continue

            new_img = os.path.basename(img_path)
            shutil.copy(img_path, f"{DEST}/images/{new_img}")

            with open(json_path) as f:
                data = json.load(f)

            if isinstance(data, dict):
                data = data.get("lines", data.get("annotations", [data]))

            for item in data:
                all_annotations.append({
                    "image": new_img,
                    "text": item.get("text") or item.get("ground_truth") or "",
                    "polygon": item.get("polygon") or item.get("bbox")
                })

with open(f"{DEST}/annotations.json", "w") as f:
    json.dump(all_annotations, f)

print("Dataset prepared ✅")
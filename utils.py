import pickle

def build_vocab(data):
    chars = set()

    for item in data:
        chars.update(list(item["text"]))

    chars = sorted(list(chars))

    char_to_idx = {c:i for i,c in enumerate(chars)}  # start from 0

    blank_index = len(chars)  # blank is LAST index

    idx_to_char = {i:c for c,i in char_to_idx.items()}

    import pickle
    pickle.dump((char_to_idx, idx_to_char), open("outputs/character_map.pkl","wb"))

    return char_to_idx, idx_to_char, blank_index
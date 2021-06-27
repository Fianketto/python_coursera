import os
import tempfile
import json
import argparse

FILENAME = "storage.data"
storage_path = os.path.join(tempfile.gettempdir(), FILENAME)


def add_key_val(storage: dict, k: str, v: str):
    cur_v = storage.get(k, [])
    cur_v.append(v)
    storage[k] = cur_v
    with open(storage_path, 'w', encoding="utf-8") as fout:
        json.dump(storage, fout)


def get_val(storage: dict, k: str):
    cur_v = storage.get(k, None)
    return_string = ""
    if cur_v:
        return_string = ", ".join(cur_v)
    return return_string


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key")
    parser.add_argument("--val")
    args = parser.parse_args()

    if args.val is None:    # get the values
        if os.path.exists(storage_path):
            fin = open(storage_path, 'r', encoding="utf-8")
            my_storage = json.load(fin)
            fin.close()
            val = get_val(my_storage, args.key)
        else:
            val = ""
        print(val)
    else:   # add key-val
        if os.path.exists(storage_path):
            fin = open(storage_path, 'r', encoding="utf-8")
            my_storage = json.load(fin)
            fin.close()
        else:
            my_storage = dict()
        add_key_val(my_storage, args.key, args.val)


if __name__ == "__main__":
    main()

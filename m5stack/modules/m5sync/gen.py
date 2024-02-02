import os
import json
from .sync import calculateMD5


def generate_json_for_directory(path, old_json=None):
    result = {}

    for entry in os.listdir(path):
        entry_path = path + "/" + entry

        info = os.stat(entry_path)
        if info[0] & 0x4000:
            result[entry] = generate_json_for_directory(
                entry_path, old_json[entry] if old_json else None
            )
        else:
            result[entry] = {
                "name": entry,
                "type": "file",
                "size": info[6],
                "mtime": info[8],
                "ext": entry.split(".")[-1] if "." in entry else "",
                "synced": False,
                "md5": calculateMD5(entry_path),
                "url": old_json[entry]["url"] if old_json else "",
            }

    return result


def generate_res_json(root_path, out_path):
    try:
        info = os.stat(out_path)
        if info[6] == 0:
            json_result = generate_json_for_directory(root_path, None)
            with open(out_path, "w") as f:
                json.dump(json_result, f)
        else:
            json_result = generate_json_for_directory(root_path, json.load(out_path))
    except:
        json_result = generate_json_for_directory(root_path, None)

    #     json_result = None
    #     if not os.path.exists(out_path):
    #         json_result = generate_json_for_directory(root_path, None)
    #     else:
    #         info = os.stat(out_path)
    #         print(info)
    #         if info[6] == 0:
    #             json_result = generate_json_for_directory(root_path, None)
    #         else:
    #             old_json = None
    #             with open(out_path) as f:
    #                 old_json = json.load(f)
    #             json_result = generate_json_for_directory(
    #                 root_path, old_json
    #             )

    with open(out_path, "w") as f:
        json.dump(json_result, f)


if __name__ == "__main__":
    generate_res_json("/flash", "res/res.json")

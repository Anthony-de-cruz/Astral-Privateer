import json

def load_map_file(file_path: str) -> dict:
    
    with open(file_path, "r") as map_file:
        map_data = json.load(map_file)

    return map_data

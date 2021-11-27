import json

def load_map_file(file_path: str) -> dict:

    """Extracts the map data out of the saved json file

    Returns:
        dict: contains map data
    """
    
    with open(file_path, "r") as map_file:
        map_data = json.load(map_file)
 
    return map_data

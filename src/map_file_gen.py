import json
import os

def generate_map(x_tiles: int, y_tiles: int) -> dict:

    grid = {}
    for y in range(y_tiles):
        for x in range(x_tiles):

            if y > 5:
                grid[f"{x},{y}"] = ["Buildable", None]
            else:
                grid[f"{x},{y}"] = ["Boundary", None]
    return grid

def main() -> None:

    map_data = generate_map(24,24)
    print(map_data)

    with open(os.path.join("levels", "map.json"), "w") as map_file:
        json.dump(map_data, map_file)

if __name__ == "__main__":

    main()

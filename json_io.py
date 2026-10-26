"""Reading and writing the JSON files (restaurant data and group requests)."""
import json


def load_restaurant(path):
    """Read the restaurant JSON and return it ready for a new evening."""
    with open(path, "r", encoding="utf-8") as f:
        restaurant = json.load(f)

    restaurant["tables"] = []
    restaurant["occupancy"] = 0
    restaurant["earnings"] = 0
    restaurant["next_table_num"] = 1
    if "allergens" not in restaurant:
        restaurant["allergens"] = {}

    return restaurant


def load_groups(path):
    """Read the JSON file with the incoming groups and return them as a list."""
    with open(path, "r", encoding="utf-8") as f:
        groups = json.load(f)

    return groups


def save_menu(restaurant, path):
    """Save the restaurant's basic info and menu back to the JSON file."""
    data = {
        "name": restaurant["name"],
        "capacity": restaurant["capacity"],
        "max_tables": restaurant["max_tables"],
        "menu": restaurant["menu"],
        "allergens": restaurant["allergens"],
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    r = load_restaurant("data/restaurant.json")
    print(r)
    g = load_groups("tables/groups1.json")
    print(g)
    save_menu(r, "data/restaurant.json")
    print("Menu saved")
# Restaurant Management System

Capstone Project (Basic Track) — Python Programming, Master's in AI & Data Science (CUNEF).

A command-line application that manages a restaurant during an evening of service. It loads incoming groups, assigns tables, takes orders, calculates bills and releases tables while tracking occupancy and earnings.

Our novel feature is allergen management: users can record declared allergens, search for compatible dishes and check each customer's allergies when taking an order.

## Team

| Member | Main responsibility | Modules |
|---|---|---|
| Pablo Montero | Reading and saving JSON files; allergen helpers | `json_io.py`, `allergens.py` |
| Javier González | Seating groups, taking orders, billing and menu operations | `restaurant_core.py` |
| Martín Monasterio | CLI menu, input validation, table selection and allergen options | `main.py` |

Integration and testing were shared across the team.

## Requirements and execution

The application uses Python 3 and the standard library. No third-party packages are required.

Open a terminal in the project folder and run:

```bash
python main.py
```

The application loads the restaurant from the fixed path:

```text
data/restaurant.json
```

Choose **1 — Load restaurant** before using the other restaurant operations.

## Project structure

```text
├── data/
│   └── restaurant.json   # persistent restaurant details, menu and allergens
├── tables/               # local group request files; ignored by Git
├── main.py               # CLI menu, validation and coordination
├── restaurant_core.py    # seating, orders, billing and menu operations
├── json_io.py            # JSON loading, validation and saving
├── allergens.py          # shared allergen parsing and compatibility checks
├── .gitignore
└── README.md
```

The `tables/` folder must be created locally if it is not present after cloning. The `.gitignore` pattern `tables*` prevents group request files in that folder from being stored in the repository.

## CLI menu

| Option | Action |
|---|---|
| 1 | Load the restaurant and start a new evening |
| 2 | Load incoming groups from a JSON file and attempt to seat each group |
| 3 | Select a seated table and take its customers' orders |
| 4 | Select an ordered table, charge it and release it |
| 5 | Add a dish or update its price and declared allergens |
| 6 | Show restaurant details, menu, allergens, tables, occupancy and earnings |
| 7 | Show dishes compatible with the allergies entered |
| 8 | Save the menu and exit |

## JSON files

### Restaurant data

The restaurant file contains its fixed information, menu prices and declared allergens. For example:

```json
{
  "name": "Demo Restaurant",
  "capacity": 20,
  "max_tables": 5,
  "menu": {
    "Pasta": 10,
    "Garden Salad": 8
  },
  "allergens": {
    "Pasta": ["gluten", "milk"],
    "Garden Salad": []
  }
}
```

The expected types are a string for `name`, positive integers for `capacity` and `max_tables`, and a dictionary of dish names and prices for `menu`.

When loading, the program checks that:

- The JSON contains an object.
- `name`, `capacity`, `max_tables` and `menu` exist.
- `menu` is an object.
- Every price is an integer or float, is finite and is greater than zero.

Data that fails these checks causes `load_restaurant()` to return `None`. The CLI displays an error and keeps any previously loaded restaurant.

If the `allergens` field is absent, it is initialized as an empty dictionary.

### Incoming groups

Create a file such as `tables/groups1.json`:

```json
[
  {"customers": 4},
  {"customers": 2},
  {"customers": 6}
]
```

Choose option 2 and enter its path.

The CLI validates the entire batch before seating anyone. Each group must be a dictionary containing a positive integer `customers` value. Boolean values are rejected.

If any group has invalid data, the whole batch is rejected. For a valid batch, each group is attempted independently: a group that does not fit does not prevent later groups from being considered.

## Table lifecycle

1. **Seated:** a group receives a table if both capacity and the maximum number of tables allow it.
2. **Ordered:** each customer is asked about allergies and chooses dishes interactively. The table becomes ordered only if at least one customer orders a dish.
3. **Charged and released:** the bill is added to earnings, occupancy is reduced and the table is removed.

If nobody at a table can order a compatible dish, the table remains seated and cannot be charged. Its order can be attempted again after the menu is extended.

Table numbers increase through `next_table_num` and are not reused during the same evening.

## Runtime data

The restaurant dictionary also holds session information:

```python
tables = []
occupancy = 0
earnings = 0
next_table_num = 1
```

These are keys inside the restaurant dictionary, not global variables.

An ordered table can look like this:

```python
table = {
    "table_num": 1,
    "customers": 2,
    "status": "ordered",
    "orders": [["Garden Salad"], ["Pasta"]],
    "allergies": [["gluten"], []]
}
```

`orders` and `allergies` contain one list per customer in the same order. `allergies` is recorded when an order is attempted. A customer's order may be empty if no compatible dish is available.

## Allergen management

Recognized names are defined in `OFFICIAL_ALLERGENS`. Input is comma-separated and case-insensitive, for example:

```text
gluten, milk
```

The parser removes surrounding spaces and duplicate valid names. Unknown names are shown to the user, who is asked to try again.

The program distinguishes:

- **Missing information (`None`):** no allergen information is available for the dish.
- **Empty list (`[]`):** no allergens have been declared for the dish.
- **Non-empty list:** the dish has the listed declared allergens.

Dishes with missing information are excluded for customers who declare allergies.

### Adding and updating dishes

- For a new dish, blank allergen input is rejected. Enter allergen names or explicitly type `none`.
- For an existing dish, pressing Enter preserves its current allergen information while updating its price.
- Entering allergen names replaces the previous declaration.
- Explicitly entering `none` replaces it with an empty list.

Dish updates ignore case differences while preserving the original menu key, so prices and allergens remain linked to the same dish.

### Taking orders and querying the menu

During an order, allergies are collected separately for each customer. Incompatible dishes are rejected.

Option 7 uses the same compatibility helpers to display matching dishes and prices. It is a query: it does not create an order or record allergies for a table.

## Module contracts

### `json_io.py`

| Function | Behavior and return value |
|---|---|
| `load_restaurant(path)` | Returns a validated restaurant dictionary with a reset evening state, or `None` if the implemented data checks fail. File-reading and JSON syntax errors are handled by the CLI. |
| `load_groups(path)` | Reads and returns JSON data. The CLI validates its structure before seating groups. |
| `save_menu(restaurant, path)` | Saves name, capacity, maximum tables, menu and allergens. Returns `None`. |

### `restaurant_core.py`

| Function | Behavior and return value |
|---|---|
| `seat_group(restaurant, customers)` | Adds a table and updates occupancy; returns the new table, or `None` if it does not fit. |
| `take_order(table, menu, allergen_info)` | Collects each customer's allergies and dishes. Returns `True` and sets status to `"ordered"` if at least one dish is ordered; otherwise returns `False` and leaves the table seated. |
| `calculate_bill(table, menu)` | Calculates and stores the bill, rounded to two decimal places, and returns it. |
| `charge_and_release(restaurant, table)` | Calculates the bill, updates earnings and occupancy, removes the table and returns the bill. |
| `add_or_update_dish(restaurant, name, price)` | Adds or updates a dish; returns `True` for a new dish and `False` for an updated dish. |

### `allergens.py`

| Function | Behavior and return value |
|---|---|
| `parse_allergies(text)` | Returns `(valid, invalid)` lists. Empty text or `none` returns two empty lists; the CLI adds context-specific rules for blank dish declarations. |
| `dish_allergens(allergens, dish)` | Returns the declared allergen list, or `None` if information is missing. |
| `conflicting_allergens(allergens, dish, allergies)` | Returns the customer's allergens that are declared for the dish. |
| `is_safe(allergens, dish, allergies)` | Returns compatibility according to the declared data; missing information is rejected for allergic customers. |
| `safe_dishes(allergens, menu, allergies)` | Returns compatible dish names, or an empty list if none match. |
| `set_dish_allergens(allergens, dish, dish_allergen_list)` | Stores a copy of the dish's allergen list. Returns `None`. |

### `main.py`

`main()` runs the menu, keeps the restaurant state and coordinates calls to the other modules.

It handles general menu input, table selection, group validation, dish input and allergen queries. Detailed customer questions during ordering are handled by `take_order()`.

## Design decisions

- Mutable restaurant state is passed through function arguments. `OFFICIAL_ALLERGENS` is a fixed reference constant.
- `done`, ignoring case, finishes a customer's order and cannot be added as a dish through the CLI.
- Bills use menu prices at charging time. Updating a price therefore affects active orders containing that dish.
- Menu changes are saved immediately after option 5 and again when exiting.
- Only restaurant configuration, menu and allergens persist. Tables, orders, occupancy and earnings restart from zero on loading.
- Option 1 reloads the restaurant and resets the current evening.
- A table is chargeable only after at least one customer has ordered.

## Limitations

- This is a local CLI application; incoming groups are simulated using files.
- An evening cannot be resumed after restarting because session data is not persisted.
- Allergen checks depend on declared information. The program does not inspect ingredients or cross-contact.
- Restaurant-file validation covers the checks listed above, rather than every possible incorrect field type or allergen declaration.

## Collaboration

The team developed features on separate branches and integrated changes through pull requests. Commits record individual contributions and integration work.

Final review changes are collected in `fix/final-review`, with separate commits for each fix, for review by another team member before merging.
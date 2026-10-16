# Restaurant Management System

Capstone Project (Basic Track) – Python Programming, Master's in AI & Data Science (CUNEF).

A command-line application that manages a restaurant during an evening of service: groups are seated, their orders are taken, and tables are charged and released, while the restaurant keeps track of its occupancy and earnings.

## Team

| Member | Module | Branch |
|---|---|---|
| Pablo Montero | `json_io.py` | `feature/json-io` |
| Javier | `restaurant_core.py` | `feature/core-logic` |
| Martín | `main.py` | `feature/cli` |

## How to run

```bash
python main.py
```

Group request files go in the `tables/` folder (ignored by Git), e.g. `tables/groups1.json`:

```json
[{"customers": 4}, {"customers": 2}, {"customers": 6}]
```

## Project structure

```
├── data/restaurant.json   # restaurant info and menu (persistent)
├── tables/                # incoming group requests (not stored in the repo)
├── main.py                # CLI: menu loop, user input and output messages
├── restaurant_core.py     # core logic: tables, orders, bills, menu
└── json_io.py             # reading and writing JSON files
```

## Table lifecycle

1. **Seated** – a group arrives and gets a table if there is room (capacity and max_tables).
2. **Ordered** – the waiter takes the order dish by dish, validated against the menu.
3. **Charged & released** – the bill is added to the earnings, the occupancy is freed and the table is removed.

## Data structures

```python
restaurant = {
    "name": str,
    "capacity": int,
    "max_tables": int,
    "menu": {dish_name: price},
    "tables": [],          # active tables
    "occupancy": 0,        # customers currently inside
    "earnings": 0,         # money earned this evening
    "next_table_num": 1    # unique table numbers, never reused
}

table = {
    "table_num": int,
    "customers": int,
    "status": "seated" | "ordered",
    "orders": []           # one list of dishes per customer
}
```

## Module contracts

### `json_io.py`
| Function | Returns |
|---|---|
| `load_restaurant(path)` | the `restaurant` dict, with an empty evening state |
| `load_groups(path)` | list of groups, e.g. `[{"customers": 4}, ...]` |
| `save_menu(restaurant, path)` | nothing; saves only name, capacity, max_tables and menu |

### `restaurant_core.py`
| Function | Returns |
|---|---|
| `seat_group(restaurant, customers)` | the new table, or `None` if it does not fit |
| `take_order(table, menu)` | nothing; asks dishes by keyboard and sets status to `"ordered"` |
| `calculate_bill(table, menu)` | the bill amount |
| `charge_and_release(restaurant, table)` | the bill; adds it to earnings, frees occupancy and removes the table |
| `add_or_update_dish(restaurant, name, price)` | `True` if the dish is new, `False` if its price was updated |

### `main.py`
`main()` runs the menu loop. It owns the `restaurant` variable and passes it to every function.

## Design rules

- **No global variables**: all data is passed through function arguments.
- **Only `main.py` prints menu messages and validates user input** (with `try/except`); the other modules return values.
- Tables are numbered with `next_table_num`, so numbers are never repeated after a table is released.
- The JSON file only stores the fixed restaurant data; the evening state (tables, occupancy, earnings) starts from zero every run.
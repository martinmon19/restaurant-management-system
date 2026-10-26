"""Allergen information: which dishes are safe for customers with allergies."""

# The 14 allergens that EU law (Regulation 1169/2011) requires restaurants to declare.
# It is a constant (never modified), not a global variable.
OFFICIAL_ALLERGENS = ("gluten", "crustaceans", "eggs", "fish", "peanuts", "soybeans", "milk",
                      "nuts", "celery", "mustard", "sesame", "sulphites", "lupin", "molluscs")


def parse_allergies(text):
    """Turn a text like 'Gluten, milk' into lists of valid and invalid allergens."""
    valid = []
    invalid = []
    if text.strip().lower() in ("", "none"):
        return valid, invalid

    for item in text.split(","):
        allergen = item.strip().lower()
        if allergen == "":
            continue
        if allergen in OFFICIAL_ALLERGENS:
            if allergen not in valid:
                valid.append(allergen)
        else:
            invalid.append(allergen)

    return valid, invalid


def dish_allergens(allergens, dish):
    """Return the allergens of a dish, or None if there is no information about it."""
    return allergens.get(dish)


def conflicting_allergens(allergens, dish, allergies):
    """Return the customer's allergens that the dish contains."""
    info = dish_allergens(allergens, dish)
    if info is None:
        return []
    conflicts = []
    for allergen in allergies:
        if allergen in info:
            conflicts.append(allergen)
    return conflicts


def is_safe(allergens, dish, allergies):
    """Check if a dish is safe for a customer with the given allergies."""
    if len(allergies) == 0:
        return True
    # Safety first: without allergen information, the dish is not served to allergic customers.
    if dish_allergens(allergens, dish) is None:
        return False
    return len(conflicting_allergens(allergens, dish, allergies)) == 0


def safe_dishes(allergens, menu, allergies):
    """Return the list of menu dishes that are safe for the given allergies."""
    safe = []
    for dish in menu:
        if is_safe(allergens, dish, allergies):
            safe.append(dish)
    return safe


def set_dish_allergens(allergens, dish, dish_allergen_list):
    """Store (or replace) the allergens of a dish."""
    allergens[dish] = list(dish_allergen_list)


if __name__ == "__main__":
    import json_io

    restaurant = json_io.load_restaurant("data/restaurant.json")
    allergens = restaurant["allergens"]

    print(parse_allergies("Gluten, milk, xyz"))
    print(parse_allergies("none"))
    print(is_safe(allergens, "Bocata de calamares", ["gluten"]))
    print(conflicting_allergens(allergens, "Bocata de calamares", ["gluten", "milk"]))
    print(safe_dishes(allergens, restaurant["menu"], ["molluscs"]))
    print(safe_dishes(allergens, restaurant["menu"], ["gluten"]))

    set_dish_allergens(allergens, "Ensalada", [])
    print(is_safe(allergens, "Ensalada", ["gluten"]))
    print(is_safe(allergens, "Plato sin info", ["gluten"]))
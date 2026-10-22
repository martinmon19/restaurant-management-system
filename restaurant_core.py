"""Core logic of the restaurant: tables, orders, bills and menu."""
def seat_group(restaurant, customers):

    if restaurant["occupancy"] + customers <= restaurant["capacity"] and (("max_tables" not in restaurant) or (restaurant["max_tables"] > len(restaurant["tables"]))): 
        table= {"table_num" : ((restaurant["next_table_num"])) , "customers" : customers, "status" : "seated", "orders":[]}
        restaurant["tables"].append
        restaurant["occupancy"] = restaurant["occupancy"] + customers
        restaurant["next_table_num"] = restaurant["next_table_num"] + 1
        return table
    else:
        return None

if __name__ == "__main__":
    import json_io
    restaurant = json_io.load_restaurant("data/restaurant.json")
    print(seat_group(restaurant, 4))
    print(seat_group(restaurant, 2))
    print(seat_group(restaurant, 60))
    print(restaurant["occupancy"], restaurant["next_table_num"])
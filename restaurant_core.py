"""Core logic of the restaurant: tables, orders, bills and menu."""
import allergens
def seat_group(restaurant, customers):

    if restaurant["occupancy"] + customers <= restaurant["capacity"] and (("max_tables" not in restaurant) or (restaurant["max_tables"] > len(restaurant["tables"]))): 
        table= {"table_num" : ((restaurant["next_table_num"])) , "customers" : customers, "status" : "seated", "orders":[]}
        restaurant["tables"].append(table)
        restaurant["occupancy"] = restaurant["occupancy"] + customers
        restaurant["next_table_num"] = restaurant["next_table_num"] + 1
        return table
    else:
        return None

def take_order(table,menu, allergen_info):
    menu_upper = {}
    for dish in menu:
        menu_upper[dish.upper()] = dish

    orders = []
    all_allergies = []
    

    for mesa in range (table["customers"]):

      while True:
        text = input(f"Does customer {mesa + 1} have any allergies?  ")
        valid, invalid = allergens.parse_allergies (text)
        if len(invalid) == 0:
           break
        print(f"Not valid: {', '.join(invalid)}")
        print(f"Valid allergens: {', '.join(allergens.OFFICIAL_ALLERGENS)}")
      all_allergies.append(valid)
      customer_orders = []
      safe = allergens.safe_dishes(allergen_info, menu, valid)
      if len(safe) == 0:
        print(f"There are no safe dishes for customer {mesa + 1}. Moving on.")
        orders.append(customer_orders)
        continue
      print("Safe dishes for this customer:")
      for dish in safe:
        print(f"  - {dish}")
      dish_ask = str(input("What do you want to eat? "))

      while dish_ask.upper() != "DONE" or len(customer_orders) < 1:
           
           if dish_ask.upper() == "DONE":
             dish_ask = str(input("You must order at least one dish: "))  
           
           elif dish_ask.upper() in menu_upper:
                dish = menu_upper[dish_ask.upper()]
                if allergens.is_safe(allergen_info, dish, valid):
                    customer_orders.append(dish)
                    dish_ask = str(input("What do you want to eat? "))
                else:
                    if allergens.dish_allergens(allergen_info, dish) is None:
                        reason = "no allergen information"
                    else:
                        reason = "contains " + ", ".join(allergens.conflicting_allergens(allergen_info, dish, valid))
                    print(f"{dish} cannot be served: {reason}.")
                    dish_ask = str(input("Choose another dish: "))
                    
           else:
               dish_ask = str(input("You have to choose an option from the menu: "))
      orders.append(customer_orders)
    
    table["orders"] = orders  
    table["allergies"] = all_allergies   
    table["status"] = "ordered"

def calculate_bill(table,menu):
    bill = 0
    for customer_orders in table["orders"]:
        for dish in customer_orders: 
         bill = bill + menu[dish]
    table["bill"] = round(bill, 2)

    return table["bill"]

def add_or_update_dish(restaurant, name, price):
    for dish in restaurant["menu"]:
        if dish.upper() == name.upper():
            restaurant["menu"][dish] = price
            return False
    restaurant["menu"][name] = price
    return True

def charge_and_release(restaurant, table):
    bill = calculate_bill(table, restaurant["menu"])
    restaurant["earnings"] = restaurant["earnings"] + bill
    restaurant["occupancy"] = restaurant["occupancy"] - table["customers"]
    restaurant["tables"].remove(table)
    return bill
if __name__ == "__main__":
    import json_io

    restaurant = json_io.load_restaurant("data/restaurant.json")
    table = seat_group(restaurant, 2)
    take_order(table, restaurant["menu"], restaurant["allergens"])
    print("Orders:", table["orders"])
    print("Allergies:", table["allergies"])
    print("Bill:", charge_and_release(restaurant, table))
    print("Earnings:", restaurant["earnings"], "Occupancy:", restaurant["occupancy"])
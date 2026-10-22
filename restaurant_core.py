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

def take_order(table,menu):
    menu_upper = {}
    for dish in menu:
        menu_upper[dish.upper()] = dish

    orders = []
    

    for mesa in range (table["customers"]):
      
        customer_orders = []
        dish_ask = str(input("What do you want to eat? "))

        while dish_ask.upper() != "DONE" or len(customer_orders) < 1:
           
           if dish_ask.upper() == "DONE":
             dish_ask = str(input("You must order at least one dish: "))  
           
           elif dish_ask.upper() in menu_upper:
               customer_orders.append(menu_upper[dish_ask.upper()])
               dish_ask = str(input("What do you want to eat? "))
           else:
               dish_ask = str(input("You have to choose an option from the menu: "))
        orders.append(customer_orders)
    table["orders"] = orders     
    table["status"] = "ordered"

def calculate_bill(table,menu):
    bill = 0
    for customer_orders in table["orders"]:
        for dish in customer_orders: 
         bill = bill + menu[dish]
    table["bill"] = bill

    return table["bill"]


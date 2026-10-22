"""Command-line interface: shows the menu and calls the other modules."""
# Importing the modules needed
import json
import json_io
import restaurant_core


# Run the main menu and coordinate the restaurant operations
def main():
    # Defining these two variables: option to select what to do and restaurant_path to simplify the path to the restaurant function
    option = 0
    restaurant_path = 'data/restaurant.json'
    restaurant = None #Making sure the user presses 1.Load restaurant first
    while option != 7:
        print('1. Load restaurant')
        print('2. Load new group requests')
        print('3. Take an order')
        print('4. Charge and release a table')
        print('5. Grow the menu')
        print('6. Check status')
        print('7. Exit')
        # Limiting the answers to a number between 1 and 7 and defining what to do in case another number is typed
        try:
            option = int(input('What do you choose?: '))
            if option < 1 or option > 7:
                print('Please choose an option from 1 to 7.')

        except ValueError:
            print('Please enter a valid number')
            continue
        
        # Perform the action selected by the user
        if option == 1:
            # Loading the restaurant and informing if there is any type of error
            try:
                restaurant = json_io.load_restaurant(restaurant_path)
                print('Restaurant loaded successfully')
            except FileNotFoundError:
                print('Im sorry, we cannot find the file')    
            except json.JSONDecodeError:
                print('Im sorry, incorrect JSON format')
        
        # Load group requests and try to seat each group
        if option == 2:
            if restaurant is None:
                print('You must load the restaurant first')
                continue
            groups_path = input('Enter the group file path (e.g. tables/groups1.json): ')

            try:
                groups = json_io.load_groups(groups_path)
            except FileNotFoundError:
                print('Group file not found.')
                continue
            except json.JSONDecodeError:
                print('Invalid JSON format in the group file.')
                continue

            for group in groups:
                table = restaurant_core.seat_group(restaurant, group['customers'])
                if table is None:
                    print(f"Group of {group['customers']} does not fit (capacity or max tables reached).")
                else:
                    print(f"Group of {group['customers']} seated at table {table['table_num']}.")

         # Take the order of a seated table
        if option == 3:
            if restaurant is None:
                print('You must load the restaurant first')
                continue
            found_table = False
            selected_table = None
            for table in restaurant['tables']:
                if table['status'] == 'seated':
                    print(f"  Table {table['table_num']} - {table['customers']} customers")
                    found_table = True
            if found_table is False:
                print('There are not any tables to be served')
                continue
            while True:
                try:
                    table_serve = int(input('What table would you like to serve: '))
                except ValueError:
                    print('Please enter a valid number.')
                    continue
                for table in restaurant['tables']:
                    if (table['table_num'] == table_serve) and table['status'] == 'seated':
                        selected_table = table
                if selected_table is None:
                    print('That table is not valid')
                    continue
                break

            print('Menu:')
            for dish in restaurant['menu']:
                print(f"  - {dish}: {restaurant['menu'][dish]}")
            print("Each customer orders dish by dish and types 'done' when finished.")
            restaurant_core.take_order(selected_table, restaurant['menu'])
            print(f"Order taken for table {selected_table['table_num']}.")

        # Charge and release a table that has already ordered
        if option == 4:
            if restaurant is None:
                print('You must load the restaurant first')
                continue
            pay_table = False
            select_table = None
            for table in restaurant['tables']:
                if table['status'] == 'ordered':
                    print(f"  Table {table['table_num']} - {table['customers']} customers - orders: {table['orders']}")
                    pay_table = True
            if pay_table is False:
                print('There are not any tables finished')
                continue
            while True:
                try:
                    table_pay = int(input('What table would you like to charge and release: '))
                except ValueError:
                    print('Please enter a valid number.')
                    continue
                for table in restaurant['tables']:
                    if (table['table_num'] == table_pay) and table['status'] == 'ordered':
                        select_table = table
                if select_table is None:
                    print('That table is not valid')
                    continue
                break

            bill = restaurant_core.charge_and_release(restaurant, select_table)
            print(f"Table {select_table['table_num']} charged: {bill}. Table released.")
            print(f"Total earnings this evening: {restaurant['earnings']}")

        #Introducing new dishes in the menu
        if option == 5:
            if restaurant is None:
                print('You must load the restaurant first')
                continue
            while True: #Repeating the question until a valid name is written
                dish_name = input('Enter the dish name: ').strip()
                if dish_name == '' or dish_name.isdigit():
                    print('Please enter a valid dish name.')
                    continue

                break   
            while True: #Same as dish name
                try:
                    price = float(input('Enter the dish price: '))
                except ValueError:
                    print('Please enter a valid number.')
                    continue

                if price <= 0:
                    print('The price must be greater than zero.')
                    continue
                break  

            is_new = restaurant_core.add_or_update_dish(restaurant, dish_name, price)
            if is_new:
                print(f"'{dish_name}' added to the menu at {price}.")
            else:
                print(f"'{dish_name}' was already on the menu. Price updated to {price}.")

            try:
                json_io.save_menu(restaurant, restaurant_path)
                print('Menu saved to file.')
            except OSError:
                print('The menu could not be saved to the file.')

        # Print the status of the restaurant
        if option == 6:
            if restaurant is None:
                print('You must load the restaurant first')
                continue

            print(f"Restaurant: {restaurant['name']}")
            print(f"Maximum capacity: {restaurant['capacity']}")
            print(f"Maximum number of tables: {restaurant['max_tables']}")
            print(f"Current occupancy: {restaurant['occupancy']}")
            print(f"Total earnings this evening: {restaurant['earnings']}")

            print('Menu:')
            for dish in restaurant['menu']:
                print(f"  - {dish}: {restaurant['menu'][dish]}")

            print('Active tables:')
            if len(restaurant['tables']) == 0:
                print('  There are no active tables.')
            for table in restaurant['tables']:
                print(f"  Table {table['table_num']} - {table['customers']} customers - {table['status']} - orders: {table['orders']}")

        # User wants to exit and save the restaurant, also what to do in case of a writing error
        if option == 7:
            if restaurant is None:
                break
            try:
                json_io.save_menu(restaurant, restaurant_path)
                print('Menu saved. Goodbye!')
            except OSError:
                print('There is a writing or access error')
                option = 0


if __name__ == "__main__":
    main()
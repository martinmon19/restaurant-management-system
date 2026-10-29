"""Command-line interface: shows the menu and calls the other modules."""
# Importing the modules needed
import json
import math
import json_io
import restaurant_core
import allergens

# Run the main menu and coordinate the restaurant operations
def main():
    # Keep the menu selection and loaded restaurant state local to main.
    option = 0
    restaurant_path = None
    restaurant = None #Making sure the user presses 1.Load restaurant first
    while option != 8:
        print('1. Load restaurant')
        print('2. Load new group requests')
        print('3. Take an order')
        print('4. Charge and release a table')
        print('5. Grow the menu')
        print('6. Check status')
        print('7. Allergen menu')
        print('8. Exit')
        # Limiting the answers to a number between 1 and 8 and defining what to do in case another number is typed
        try:
            option = int(input('What do you choose?: '))
            if option < 1 or option > 8:
                print('Please choose an option from 1 to 8.')
                continue

        except ValueError:
            print('Please enter a valid number')
            continue
        
        # Perform the action selected by the user
        if option == 1:
            # Select a file; keep the current restaurant if the new load fails.
            selected_path = input('Enter the restaurant file path (e.g. data/restaurant.json): ').strip()
            if selected_path == '':
                print('Please enter a restaurant file path.')
                continue
            try:
                loaded_restaurant = json_io.load_restaurant(selected_path)
                if loaded_restaurant is None:
                    print('Invalid restaurant data.')
                else:
                    restaurant = loaded_restaurant
                    restaurant_path = selected_path
                    print('Restaurant loaded successfully')
            except FileNotFoundError:
                print('Im sorry, we cannot find the file')    
            except json.JSONDecodeError:
                print('Im sorry, incorrect JSON format')
            except (OSError, UnicodeError):
                print('The restaurant file could not be read.')
        
        # Load group requests and try to seat each group
        if option == 2:
            if restaurant is None:
                print('You must load the restaurant first')
                continue
            groups_path = input('Enter the group file path (e.g. tables/groups1.json): ').strip()

            try:
                groups = json_io.load_groups(groups_path)
            except FileNotFoundError:
                print('Group file not found.')
                continue
            except json.JSONDecodeError:
                print('Invalid JSON format in the group file.')
                continue
            except (OSError, UnicodeError):
                print('The group file could not be read.')
                continue

            if not isinstance(groups, list):
                print('The group file must contain a list of groups.')
                continue

            # Validate the whole batch before seating any groups.
            valid_groups = True
            for group in groups:
                if not isinstance(group, dict):
                    valid_groups = False
                    break
                if 'customers' not in group:
                    valid_groups = False
                    break
                customers = group['customers']
                if type(customers) is not int or customers <= 0:
                    valid_groups = False
                    break

            if  valid_groups is False:
                print('Each group must contain a positive whole number of customers.')
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
            taken = restaurant_core.take_order(selected_table, restaurant['menu'], restaurant['allergens'])
            if taken is True:
                print(f"Order taken for table {selected_table['table_num']}.")
            else:
                print('Nobody at this table can eat any dish of the current menu. The table stays seated.')

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
                if dish_name.lower() == 'done':
                    print("'done' is reserved for finishing an order. Please choose another dish name.")
                    continue

                break   
            while True: #Same as dish name
                try:
                    price = float(input('Enter the dish price: '))
                except ValueError:
                    print('Please enter a valid number.')
                    continue

                if not math.isfinite(price) or price <= 0:
                    print('The price must be a finite number greater than zero.')
                    continue
                break  
            
            existing_name = None
            for names in restaurant['menu']:
                if dish_name.upper() == names.upper():
                    existing_name = names
                    break
            keep_allergens = False                 
            while True:
                if existing_name is not None:
                    allergen_text = input('Allergens of the dish (comma separated, or none, Enter to keep the current ones): ')
                    if allergen_text.strip() == '':
                        keep_allergens = True
                        break
                else:
                    allergen_text = input('Allergens of the dish (comma separated, or none): ') 
                    if allergen_text.strip() == '':
                        print("Please type the allergens, or 'none' if the dish has no allergens.")
                        continue           
                valid, invalid = allergens.parse_allergies(allergen_text)
                if len(invalid) > 0:
                    print(invalid)
                    print(allergens.OFFICIAL_ALLERGENS)
                    continue
                else:
                    break
            is_new = restaurant_core.add_or_update_dish(restaurant, dish_name, price)
            if is_new is True:
                print(f"'{dish_name}' added to the menu at {price}.")
            else:
                print(f"'{dish_name}' was already on the menu. Price updated to {price}.")
                
            for dishes in restaurant['menu']:
                if dishes.upper() == dish_name.upper():
                    actual_dish_name = dishes
                    break   
                    
            if  keep_allergens is False:
                allergens.set_dish_allergens(restaurant['allergens'], actual_dish_name, valid)


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
                info = allergens.dish_allergens(restaurant['allergens'], dish)
                if info is None:
                    print('No allergen information')
                elif len(info) == 0:
                    print('No declared allergens')
                else:
                    print(info)
            print('Active tables:')
            if len(restaurant['tables']) == 0:
                print('  There are no active tables.')
            for table in restaurant['tables']:
                print(f"  Table {table['table_num']} - {table['customers']} customers - {table['status']} - orders: {table['orders']}")
                table_allergies = table.get('allergies')
                if table_allergies is None:
                    print('Allergies not recorded yet')
                else:
                    print(table_allergies)
        # Show dishes compatible with the customer's allergies
        if option == 7:
            if restaurant is None:
                print('You must load the restaurant first')
                continue
            while True:# Ask for allergies and repeat until all names are valid
                allergen_costumer = input('Allergens of the costumer (comma separated, or none): ')
                valid, invalid = allergens.parse_allergies(allergen_costumer)
                if len(invalid) > 0:
                    print(invalid)
                    print(allergens.OFFICIAL_ALLERGENS)
                    continue
                else:
                    break
           
            valid_dishes = allergens.safe_dishes(restaurant['allergens'], restaurant['menu'], valid)
            if len(valid_dishes) <= 0:
                print('Sorry, there are no dishes available for you')
            else:
                for dishes in valid_dishes:
                    print(dishes, restaurant['menu'][dishes])

        # User wants to exit and save the restaurant, also what to do in case of a writing error
        if option == 8:
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
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
                print('Restaurant loaded succesfully')
            except FileNotFoundError:
                print('Im sorry, we cannot find the file')    
            except json.JSONDecodeError:
                print('Im sorry, incorrect JSON format')
        
        # Add group request loading and handle file errors
        if option == 2:
            if restaurant is None:
                print('You must load the restaurant first')
                continue
            groups_path = input('Enter the group file path: ')
            
            try:
                groups = json_io.load_groups(groups_path)
            except FileNotFoundError:
                print('Group file not found.')               
            except json.JSONDecodeError:
                print('Invalid JSON format in the group file.')
        
        #Taking an order
        if option == 3:
            if restaurant is None:
                print('You must load the restaurant first')
                continue
            found_table = False
            selected_table = None
            for table in restaurant['tables']:
                if table['status'] == 'seated':
                    print(table)
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
        
        #Charging and realising tables    
        if option == 4:
            if restaurant is None:
                print('You must load the restaurant first')
                continue
            pay_table = False
            select_table = None
            for table in restaurant['tables']:
                if table['status'] == 'ordered':
                    print(table)
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
            if dish_name in restaurant['menu']:
                if price == restaurant['menu'][dish_name]:
                    print('This dish already has that price.')
                    continue
                else:
                    print('This dish is already on the menu. Its price will be updated.')  
                
                
        # Print the status of the restaurant
        if option == 6:
            if restaurant is None:
                print('You must load the restaurant first')
                continue
    
            print(f' You have selected restaurant: {restaurant['name']}')
            print(f' The maximum capacity is: {restaurant['capacity']}')
            print(f' The maximum number of tables is: {restaurant['max_tables']}')
            print(f' The curent occupancy is: {restaurant['occupancy']}')
            print(f' Total earnings for the day are: {restaurant['earnings']}')
            
            for plates in restaurant['menu']:
                print(plates, restaurant['menu'][plates])
            
            for services in restaurant['tables']:
                print(services) 
        
        # User wants to exit and save the restaurant, also what to do in case of name error    
        if option == 7:
            if restaurant is None:
                break
            try:
                json_io.save_menu(restaurant, restaurant_path)
            except OSError:
                print('There is a writing or acces error')
                option = 0
                
            
                
                
          
main()          
          
                    
      
    
        
        
        
        
    
   

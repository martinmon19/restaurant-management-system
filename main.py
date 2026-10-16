"""Command-line interface: shows the menu and calls the other modules."""
def main():
    option = 0

    while option != 7:
        print('1. Load restaurant')
        print('2. Load new group requests')
        print('3. Take an order')
        print('4. Charge and release a table')
        print('5. Grow the menu')
        print('6. Check status')
        print('7. Exit')
        try:
            option = int(input('What do you choose?: '))
            if option < 1 or option > 7:
                print('Please choose an option from 1 to 7.')
            if option == 7:
                break
        except ValueError:
            print('Please enter a valid number')
                
      
    
        
        
        
        
    
main()    

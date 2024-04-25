
"""
    We want to manage a vegan product store. This program has the following functions:
        - list: to get a list of products in stock, quantities, and prices
        - add: to add new products to the inventory or add new quantities of a product if it's already available
        - sale: to sell a single product to a customer and record the sale in the cumulative sales register
        - profits: to return the store's profits at various levels of detail (total store, all products one by one, and for a single product)
"""

"""
    I chose to use a json file for saving data, to make it easy to navigate both sections visually:
        - inventory: to keep track of information related to inventory
        - aggregate sales: to keep track of information related to sales and profits
    Each product is stored in each section as a dictionary. This structure allows us to modify any data inside it, including prices. In the future, we plan to add a section to program discounts and modify prices in anticipation of cost increases.
"""

"""
    I import the necessary modules:
        - json to operate on the selected file type for saving data
        - os to check if the file already exists in the working directory
"""
import json
import os

# I use a variable to keep track of whether I find the prepared json file for saving information or not
found = False

def write_file(store):
    with open("inventory.json", "w") as json_file:
        json.dump(store, json_file, indent=3)

def read_file():
    with open("inventory.json", "r") as json_file:
        store = json.load(json_file)
    return store

# I start a loop that goes through all the files in the working directory and checks if I find the saving file
for i in range(len(os.listdir())):
    if os.listdir()[i] == "inventory.json":
        found = True

#If I don't find the saving file, I create it
if not found:
    store = {"inventory": {}, "aggregate_sales": {}}
    write_file(store)
    





#This function will be used to check if an input that must be a number is actually numeric. If the parameter "floor" is given, the input cannot be less than that value. By default, floor is set to 0.
def validate_number(floor=0):
    good_input = False
    while not good_input:
        try:
            input_value = float(input())
            if input_value > floor:
                good_input = True
            else:
                print(f"The number must be greater than {floor}. Please try again: ")
        except ValueError:
            print("Please enter a number. Please try again: ")

    return input_value

#This function will be used to check if an input matches the available commands.
def validate_choice(option_1=True, option_2=True, option_3=True):
    good_input = False
    while not good_input:
        command = input()
        if command == option_1 or command == option_2 or command == option_3:
            good_input = True
        else:
            print("The entered command is not among the allowed options. Please try again: ")
    return command








def add():
    
    print("\nWelcome to the function to add new products or add quantity to existing products\n")
    
    # open file in read mode and assign to a variable
    store = read_file()
    
    # create a control variable for continuous product entry
    continue_adding = "y"
    
    # with this loop, I continue adding products until the user responds with no (n)
    while continue_adding != "n":
        
        # get all the names of the products already registered in the inventory
        registered_products = list(store["inventory"].keys())
    
        # input the name of the product to register or update
        product_name = input("Enter the name of the product to add to the inventory or update for quantity: ")
        
        """
        After obtaining the product name, check if it already exists. If it does, update the quantity in inventory. 
        If it doesn't, add a new product
        """
        if product_name in registered_products:
            
            """
            The product is already registered. 
            Get the quantity of product to add, 
            check that the quantity entered is positive and greater than 0. 
            If not, print an exception on the screen and ask for the value again.
            """
            print("Enter the quantity of product to add to the existing quantity")
            quantity_to_add = validate_number(floor=0)
            
            # add the new quantity to what we already had in inventory
            product_quantity = quantity_to_add + store["inventory"][product_name]["quantity"]
            
            # leave the purchase and sale prices unchanged
            purchase_price = store["inventory"][product_name]["purchase_price"]
            sale_price = store["inventory"][product_name]["sale_price"]
            
        else: 
            
            """
            The selected product does not exist yet.
            Input the other inventory variables: quantity, purchase price, sale price. 
            Check that each of them is positive and greater than 0. 
            In particular, it is required that the sale price is greater than the purchase price so as not to incur losses. 
            If they don't meet the rules, print an error message and ask for re-entry.
            """
            # input the quantity
            print("Enter the quantity of the product to add to the inventory")
            product_quantity = int(validate_number(floor=0))
             
            # input the purchase price for the store       
            print("Enter the purchase price of the product")
            purchase_price = round(validate_number(floor=0), 2)
            
            # input the sale price       
            print("Enter the sale price of the product")
            sale_price = round(validate_number(floor=purchase_price), 2)
            
        # insert the input variables into the dictionary
        store["inventory"][product_name.lower()] = {"quantity": product_quantity, "purchase_price": purchase_price, "sale_price": sale_price}
        
        """
        Ask the user if they want to enter new products 
        and verify if it is one of the two possible choices.
        If they make a mistake, keep asking until they choose between y and n
        """
        print("Enter y to continue adding and n to stop adding")
        continue_adding = validate_choice(option_1="y", option_2="n")
    
    # at the end of the entries, save everything to the file 
    write_file(store)





    
def list_of_products():
    
    print("\nWelcome to the function for listing the products present in the warehouse. Here you can choose to list only the names of the products or the entire warehouse details.\n")
    
    # open the file in read mode
    store = read_file()
    
    # get the list of keys (product names) in the warehouse
    products = list(store["inventory"].keys())
    
    # get the user input for what kind of listing they want
    print("Enter:\n - 'products' if you want only the list of products present in the warehouse\n - 'details' if you want the warehouse details with products, quantities, and prices\n")
    choice = validate_choice(option_1="products", option_2="details")
    
    # check the user's listing choice and based on that, print the different information obtained on the screen
    if choice.lower() == "products":
        print("Here's the list of all the products present in the warehouse:\n")
        
        # using a for loop, iterate over all the keys in the warehouse to print them as the respective product names
        for i in range(0, len(products)):
            print(products[i])
            
    else:
        print("Here's the detail of the entire warehouse:\n")
        
        # using a for loop, iterate over all the keys in the warehouse to print the respective details of the registered products
        for i in range(0, len(products)):
            
            # get the respective details of quantity and prices for each product
            quantity = store["inventory"][products[i]]["quantity"]
            purchase_price = store["inventory"][products[i]]["purchase_price"]
            sales_price = store["inventory"][products[i]]["sale_price"]
            
            # print a user-friendly sentence to communicate the warehouse details
            print(f"The product '{products[i]}' is present in the warehouse with a quantity of {quantity}. It was purchased at {purchase_price} and is sold at {sales_price}")

    
    
def sale():
    
    print("\nWelcome to the store's salt department\nHere you can sell the products chosen by the customer:\n")
    
    # Open the file in read mode
    store = read_file()
        
    # Get all the products, as keys, from the inventory
    registered_products = list(store["inventory"].keys())
    
    # Get all the products, as keys, from the aggregated sales
    sold_products = list(store["aggregate_sales"].keys())
    
    # Check the input for the product to buy
    good_input = False
    while not good_input:
        try:
            # Get the name of the product to buy as input
            product_name = input("Enter the name of the product to buy: ")
            
            # Get the corresponding quantity in the inventory
            inventory_quantity = store["inventory"][product_name]["quantity"]
            
            # If the product is present in inventory and has a quantity greater than 0, it can be purchased
            # Otherwise, print error messages based on the user's choice
            if product_name in registered_products and inventory_quantity > 0:
                good_input = True
            else:
                print("The product is not currently available. \nPlease choose another one\n")
        except KeyError:
            # Create an error message for 'KeyError' because the input is used as the search key
            # If this key does not match any of the available keys, print a custom error message for that case
            print("Non-existent product. \nRequest the list of products and try the purchase again\n")
    
    # Get the desired quantity of the product as input and check that it meets the following requirements:
    # - be a positive number
    # - be greater than or equal to the quantity of the product available in inventory
    good_input = False
    while not good_input:
        try:
            product_quantity = int(input("Enter the quantity of the product to buy: "))
            if product_quantity > 0:
                if product_quantity <= inventory_quantity:
                    good_input = True
                else:
                    print(f"You can choose a maximum quantity of {inventory_quantity}")
            else:
                print("The number must be positive and greater than 0. Try again: ")
        except ValueError:
            print("A number is required. Try again: ")
    
    # Calculate the new quantity of the product available in inventory        
    inventory_quantity = inventory_quantity - product_quantity
    
    # Get the prices related to the selected product from the inventory
    purchase_price = store["inventory"][product_name]["purchase_price"]
    selling_price = store["inventory"][product_name]["sale_price"]
    
    # Update the inventory with the new quantity
    store["inventory"][product_name.lower()] = {"quantity": inventory_quantity, "purchase_price": purchase_price, "sale_price":selling_price}
    
    # Calculate the gross profit made from selling the product by doing quantity * selling_price (gross because the product costs haven't been deducted yet)
    gross_profit = round(selling_price * product_quantity, 2)
    
    # Calculate the net profit obtained from the difference between the selling and purchase prices for the respective quantity sold
    net_profit = round((selling_price - purchase_price) * product_quantity, 2)

    # Check if the product the customer is buying is already available in the sales register
    if product_name in sold_products:
        
        # The product is already present in the sales register
        # Get the old quantity of the product sold and add the new sale
        old_quantity = store["aggregate_sales"][product_name.lower()]["quantity"]
        new_quantity = old_quantity + product_quantity
        
        
        old_gross_profit = store["aggregate_sales"][product_name.lower()]["gross_profit"]
        new_gross_profit = old_gross_profit + gross_profit
    
        # Get the old net profit of the sold product and add the new one 
        old_net_profit = store["aggregate_sales"][product_name.lower()]["net_profit"]
        new_net_profit = old_net_profit + net_profit
        
        # Add everything to the dictionary
        store["aggregate_sales"][product_name.lower()] = { "quantity": new_quantity, "gross_profit": new_gross_profit, "net_profit":new_net_profit}
    else:
    
        # The product was not among the sales so I insert it
        store["aggregate_sales"][product_name.lower()] = { "quantity": product_quantity, "gross_profit": gross_profit, "net_profit":net_profit}

    # Print a message to the user with the sales report
    print (f"The customer bought the product {product_name} with a quantity of {product_quantity} for a total value of {gross_profit}\n")


    if inventory_quantity == 0:
        store["magazzino"].pop(product_name)

    # At the end of the inserts, save everything to the file 
    write_file(store)


    
    
    
            
    
            
    
    
def profits():
    print("welcome to the profits function")
    
    # open file in read mode
    store = read_file()
    
    # get keys of individual products which are registered as sold
    sold_products = list(store["aggregate_sales"].keys())
    
    # get input for what type of detail is wanted for the sales department
    # check if input follows allowed commands, if not request a new input until the input follows the allowed commands
    print("enter:\n - 'aggregate' if you want the aggregate of the whole store \n - 'detail' if you want the profits of each individual product \n - 'single product': if you want the profits of a single product\n")
    choice = validate_choice(option_1="aggregate", option_2="detail", option_3="single product")
    
    # check what detail choice the user made
    if choice.lower() == "aggregate":
        
        # initialize variables to get registered data
        total_gross_profits = 0
        total_net_profits = 0
        total_sales_quantity = 0

        # iterate over all products
        for i in range(0, len(sold_products)):
            
            # get all data of the sales register and aggregate them to have the total of the store
            total_gross_profits += store["aggregate_sales"][sold_products[i]]["gross_profit"]
            total_net_profits += store["aggregate_sales"][sold_products[i]]["net_profit"]
            total_sales_quantity += store["aggregate_sales"][sold_products[i]]["quantity"]
        
        # print a message to provide the store's sales values to the user
        print(f"The store has sold a total quantity of products equal to {total_sales_quantity}, collecting {total_gross_profits} and earning {total_net_profits}")
            
    elif choice.lower() == "detail":
        
        for i in range(0, len(sold_products)):
            
            # for each product get the profits and quantity data
            quantity = store["aggregate_sales"][sold_products[i]]["quantity"]
            gross_profit = store["aggregate_sales"][sold_products[i]]["gross_profit"]
            net_profit = store["aggregate_sales"][sold_products[i]]["net_profit"]
            
            # print on screen the data of each product
            print(f"for the product '{sold_products[i]}' a quantity of {quantity} has been sold, collecting {gross_profit} and earning {net_profit}")
    else:
        
        good_input = False
        while not good_input:
            
            # ask the user which product they want to know the sales of, so as to understand whether they are selling it or not
            chosen_product = input("choose a product for which you want to know the sales: \n")
            if chosen_product in sold_products:
                good_input = True
            else:
                print("the chosen product has never been sold")
        
        # get details of the chosen product
        quantity = store["aggregate_sales"][chosen_product.lower()]["quantity"]
        gross_profit = store["aggregate_sales"][chosen_product.lower()]["gross_profit"]
        net_profit = store["aggregate_sales"][chosen_product.lower()]["net_profit"]
        
        # communicate to the user the details of the chosen product
        print(f"for the product '{chosen_product.lower()}' a quantity of {quantity} has been sold, collecting {gross_profit} and earning {net_profit}")
     
            
            

    
    
    
    
def close():
    print("\nThe program is closing.\nThank you and goodbye!\n")
    
def help():
    print("""These are all the available commands and their functions:
          - add: add a product to the warehouse  
          - list of products: list the products in the warehouse  
          - sale: record a sale made  
          - profits: show the total profits  
          - close: exit the program""")




        
# control variable of the while loop and on which I perform comparisons to access various menus
command = ""

while command.lower() != "close":
    
    command = input("if you don't know the commands, type 'help'\nPlease enter the selected command: \n")

    if command.lower() == "add":
        add()
    elif command.lower() == "list of products":
        list_of_products()
    elif command.lower() == "sale":
        sale()
    elif command.lower() == "profits":
        profits()
    elif command.lower() == "help":
        help()
    elif command.lower() == "close":
        close()
    else:
        print("invalid command entered")
# ========== The beginning of the class ==========

class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        # Defensive: ensure cost and quantity are stored as correct types
        self.cost = float(cost)  #cost will be in decimals
        self.quantity = int(quantity)

    def get_cost(self): #get the cost of the shoes
        return self.cost

    def get_quantity(self): #get the quantity of stock on hand
        return self.quantity

    def __str__(self): #return a string representation of the class Shoe
        return (
            f"Country:  {self.country}\n"
            f"Code:     {self.code}\n"
            f"Product:  {self.product}\n"
            f"Cost:     {self.cost:.2f}\n"
            f"Quantity: {self.quantity}\n"
        )

# ============= Shoe list ===========

shoe_list = []

inventory_file = "inventory.txt"

def save_shoes_to_file(): #add new items to inventory file
    try:
        with open(inventory_file, "w", encoding="utf-8") as file:
            file.write("country,code,product,cost,quantity\n")
            for shoe in shoe_list: # Write each shoe as a CSV row
                line = (
                    f"{shoe.country},"
                    f"{shoe.code},"
                    f"{shoe.product},"
                    f"{shoe.cost},"
                    f"{shoe.quantity}\n"
                )
                file.write(line)
    except Exception as e:
        print(f"An error occurred while saving to the inventory: {e}")

# ========== Functions outside the class ==============

def read_shoes_data():
    
    #Opens inventory.txt - reads data - creates a shoes object - append the object into the shoes list.
   # Here a try-except is used for error handling. 
 
    shoe_list.clear()

    try:
        with open(inventory_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        if len(lines) <= 1: # Check if file has shoe data other then the header
            print("The inventory file contains no shoe data (only header).")
            return
        
        for line in lines[1:]:  # Skip the header (index 0) and process remaining lines
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            items = line.split(",")

            # Defensive: ensure correct number of columns
            if len(items) != 5:
                print(f"Skipping malformed line: {line}")
                continue

            country, code, product, cost_str, quantity_str = items

            try:
                cost = float(cost_str)
                quantity = int(quantity_str)
            except ValueError:
                print(f"Skipping line with invalid numeric data: {line}")
                continue

            shoe = Shoe(
                country.strip(),
                code.strip(),
                product.strip(),
                cost,
                quantity
            )
            shoe_list.append(shoe)

        print("Shoe data is loaded successfully into the inventory file.")

    except FileNotFoundError:
        print(f"Error: The file '{inventory_file}' was not found.")
        print("Please make sure the file exists in the correct directory.")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")

def capture_shoes():  #capture data about a shoe and create a shoe object - append into shoe list
    print("\n--- Capture New Shoe Information---")
    country = input("Enter country: ").strip()
    code = input("Enter shoe code: ").strip()
    product = input("Enter product name: ").strip()
   
    while True:   # Defensive coding: cost must be a valid number
        cost_input = input("Enter cost (e.g. 1500.00): ").strip()
        try:
            cost = float(cost_input)
            if cost < 0:
                print("Cost cannot be negative. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please check and re-enter corrcet value for cost.")

    while True:  # Defensive coding: quantity must be a valid positive number
        quantity_input = input("Enter shoe quantity: ").strip()
        try:
            quantity = int(quantity_input)
            if quantity < 0:
                print("Quantity cannot be less than zero. Please reenter quantity.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number for quantity.")

    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)
    
    save_shoes_to_file()  #Save new shoe to file

    print("\nNew shoe captured and saved successfully:")
    print(new_shoe)

def view_all(): #iterate shoes list, print details from the __str__function == tabulate
    if not shoe_list:
        print("No shoes to display. Please load data or capture new shoes.")
        return

    print("\n--- All Shoes in Inventory ---")
    for index, shoe in enumerate(shoe_list, start=1):
        print(f"Shoe #{index}")
        print(shoe)
        print("-" * 40)

def re_stock(): #Find shoe object with the lowest quantity, for re-stocking, request quantity and update list.
    if not shoe_list:
        print("No shoes available. Please load data or capture shoes first.")
        return
    
    shoe_to_restock = min(shoe_list, key=lambda s: s.get_quantity()) # Find shoe with the lowest quantity

    print("\n--- Restock ---")
    print("Shoe with the lowest quantity:")
    print(shoe_to_restock)

    choice = input("Do you want to restock this shoe? (y/n): ").strip().lower()
    if choice != "y":
        print("Restock item cancelled.")
        return
    
    while True:  # Defensive: quantity to add must be a positive integer
        amount_input = input("Enter quantity to be restocked: ").strip()
        try:
            amount = int(amount_input)
            if amount <= 0:
                print("Please enter a positive whole number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    shoe_to_restock.quantity += amount
    
    save_shoes_to_file()  # Save updated quantities back to file

    print("\nShoe restocked successfully. Updated details:")
    print(shoe_to_restock)

def search_shoe():  #search a shoe using the shoe code, return this object for printing.
    if not shoe_list:
        print("No shoes available. Please load data or capture shoes first.")
        return

    code = input("\nEnter shoe code to search: ").strip().upper()

    for shoe in shoe_list:
        if shoe.code.upper() == code:
            print("\nShoe found:")
            print(shoe)
            return

    print("No shoe found with that code. Try again.")

def value_per_item():  #Calculate the total value for each shoe item. Note: value = cost * quantity.
    if not shoe_list:
        print("No shoes available. Please load data or capture shoes first.")
        return

    print("\n--- Value per Shoe Item ---")
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        print(
            f"Code: {shoe.code} | "
            f"Product: {shoe.product} | "
            f"Cost: {shoe.get_cost():.2f} | "
            f"Quantity: {shoe.get_quantity()} | "
            f"Total Value: {value:.2f}"
        )
    print("-" * 40)

def highest_qty():  #Identify shoe with highest quantity and print this shoe as being for sale.
    if not shoe_list:
        print("No shoes available. Please load data or capture shoes first.")
        return

    shoe_with_highest = max(shoe_list, key=lambda s: s.get_quantity())

    print("\n--- Product with Highest Quantity ---")
    print("This shoe is on SALE!")
    print(shoe_with_highest)

# ========== Main Menu =============

def main_menu():  #Create a menu for executing each function - using the loop function. 
    print("Welcome to the Nike Warehouse Inventory System!")
    read_shoes_data()  #Load data at the start

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Reload shoe data from file")
        print("2. Capture a new shoe")
        print("3. View all shoes")
        print("4. Restock lowest-quantity shoe")
        print("5. Search shoe by code")
        print("6. View value per item")
        print("7. View product with highest quantity (for sale)")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            read_shoes_data()
        elif choice == "2":
            capture_shoes()
        elif choice == "3":
            view_all()
        elif choice == "4":
            re_stock()
        elif choice == "5":
            search_shoe()
        elif choice == "6":
            value_per_item()
        elif choice == "7":
            highest_qty()
        elif choice == "8":
            print("Thank you. Exiting programme. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main_menu()

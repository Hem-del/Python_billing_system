import os
import csv
from datetime import datetime

# File paths
ITEMS_FILE = "items.csv"
TRANSACTIONS_FILE = "transactions.csv"

# Initialize CSV files
def initialize_files():
    try:
        with open(ITEMS_FILE, mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Price"])
    except FileExistsError:
        pass

    try:
        with open(TRANSACTIONS_FILE, mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Bill No", "Date", "Time", "Transaction Type", "Total Amount", "Details"])
    except FileExistsError:
        pass

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Read CSV file
def read_csv(file_path):
    try:
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please initialize the system.")
        return []

# Write CSV file
def write_csv(file_path, rows, mode="w"):
    try:
        with open(file_path, mode=mode, newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

# Main Menu
def main_menu():
    while True:
        clear_screen()
        print("Main Menu")
        print("1. Admin Dashboard")
        print("2. Bill Generator")
        print("3. History")
        print("4. Exit")
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            admin_dashboard()
        elif choice == "2":
            bill_generator()
        elif choice == "3":
            view_history()
        elif choice == "4":
            print("Exiting the system...")
            break
        else:
            print("Invalid option. Please try again.")

# Admin Dashboard
def admin_dashboard():
    clear_screen()
    username = input("Username: ")
    password = input("Password: ")

    if username == "admin" and password == "admin":
        print("Login Successful!")
        input("Press Enter to continue to the Admin Panel...")
        admin_panel()
    else:
        print("Incorrect username or password. Try again.")
        input("Press Enter to return to the main menu...")

# Admin Panel
def admin_panel():
    global cgst_rate, sgst_rate
    while True:
        clear_screen()
        print("Admin Dashboard")
        print(f"CGST Rate: {cgst_rate}% | SGST Rate: {sgst_rate}%")
        print("1. Show Existing Items")
        print("2. Add New Item")
        print("3. Modify Existing Item")
        print("4. Delete Existing Item")
        print("5. Update CGST Rate")
        print("6. Update SGST Rate")
        print("7. Go Back to Main Menu")
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            show_existing_items()
        elif choice == "2":
            add_new_item()
        elif choice == "3":
            modify_existing_item()
        elif choice == "4":
            delete_existing_item()
        elif choice == "5":
            update_cgst_rate()
        elif choice == "6":
            update_sgst_rate()
        elif choice == "7":
            break
        else:
            print("Invalid option. Please try again.")

# Show Existing Items
def show_existing_items():
    clear_screen()
    items = read_csv(ITEMS_FILE)
    if len(items) <= 1:
        print("No items found.")
    else:
        print("Existing Items:")
        for item in items[1:]:  # Skip the header row
            print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}")
    input("Press Enter to return to the admin dashboard...")

# Modify Existing Item
def modify_existing_item():
    clear_screen()
    items = read_csv(ITEMS_FILE)
    
    if len(items) <= 1:
        print("No items found.")
        input("Press Enter to return to the admin dashboard...")
        return

    print("Existing Items:")
    for item in items[1:]:  # Skip the header row
        print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}")

    item_id = input("Enter the ID of the item you want to modify: ").strip()
    
    # Find item to modify
    for i, item in enumerate(items[1:], start=1):  # Skip header row
        if item[0] == item_id:
            print(f"Selected Item: ID: {item[0]}, Name: {item[1]}, Price: {item[2]}")
            new_name = input(f"Enter new name (leave blank to keep '{item[1]}'): ").strip()
            new_price = input(f"Enter new price (leave blank to keep '{item[2]}'): ").strip()

            # Update name and price only if values are provided
            if new_name:
                items[i][1] = new_name
            if new_price:
                try:
                    items[i][2] = f"{float(new_price):.2f}"
                except ValueError:
                    print("Invalid price. No changes made to the price.")
            
            write_csv(ITEMS_FILE, items)
            print("Item modified successfully!")
            input("Press Enter to return to the admin dashboard...")
            return

    print("Invalid item ID. No changes made.")
    input("Press Enter to return to the admin dashboard...")
    
# Add New Item
def add_new_item():
    clear_screen()
    items = read_csv(ITEMS_FILE)
    new_id = len(items)
    name = input("Enter item name: ").strip()
    price = input("Enter item price: ").strip()
    items.append([new_id, name, price])
    write_csv(ITEMS_FILE, items)
    print(f"Item '{name}' added successfully.")
    input("Press Enter to return to the admin dashboard...")

# Bill Generator
def bill_generator():
    clear_screen()
    items = read_csv(ITEMS_FILE)
    if len(items) <= 1:
        print("No items available for billing.")
        input("Press Enter to return to the main menu...")
        return

    print("Available Items:")
    for item in items[1:]:  # Skip the header row
        print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}")

    cart = []
    while True:
        item_id = input("Enter item ID to add to the bill (or 'done' to finish): ").strip()
        if item_id.lower() == "done":
            break

        quantity = input("Enter quantity: ").strip()
        for item in items[1:]:
            if item[0] == item_id:
                cart.append((item[1], float(item[2]), int(quantity)))
                print(f"Added {quantity} x {item[1]} to the cart.")
                break
        else:
            print("Invalid item ID. Please try again.")

    if not cart:
        print("No items added to the bill.")
        input("Press Enter to return to the main menu...")
        return

    # Generate bill
    total = sum(price * qty for _, price, qty in cart)
    cgst = total * cgst_rate / 100
    sgst = total * sgst_rate / 100
    grand_total = total + cgst + sgst

    print("\n--- Bill Summary ---")
    for name, price, qty in cart:
        print(f"{qty} x {name} @ {price:.2f} = {price * qty:.2f}")
    print(f"Subtotal: {total:.2f}")
    print(f"CGST ({cgst_rate}%): {cgst:.2f}")
    print(f"SGST ({sgst_rate}%): {sgst:.2f}")
    print(f"Grand Total: {grand_total:.2f}")

    # Save transaction
    transaction_details = [{"Item": name, "Price": price, "Quantity": qty} for name, price, qty in cart]
    transactions = read_csv(TRANSACTIONS_FILE)
    bill_no = len(transactions)
    now = datetime.now()
    transactions.append([
        bill_no,
        now.strftime("%Y-%m-%d"),
        now.strftime("%H:%M:%S"),
        "Sale",
        f"{grand_total:.2f}",
        str(transaction_details),
    ])
    write_csv(TRANSACTIONS_FILE, transactions)
    print(f"Bill No. {bill_no} saved successfully!")
    input("Press Enter to return to the main menu...")
# Clear Screen Function
def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

# View History Function
def view_history():
    clear_screen()
    transactions = read_csv(TRANSACTIONS_FILE)

    if len(transactions) <= 1:
        print("No transaction history found.")
        input("Press Enter to return to the main menu...")
    else:
        while True:
            clear_screen()
            print("Transaction History")
            print("1. View Summary of All Bills")
            print("2. View Detailed Bill of a Specific Transaction")
            print("3. Return to Main Menu")
            choice = input("Select an option: ").strip()

            if choice == "1":
                # Display summary of all bills
                clear_screen()
                print("---- Bill Summary ----")
                print("{:<10} {:<15} {:<15} {:<10}".format("Bill No", "Date", "Time", "Total Amount"))
                print("-" * 50)
                for row in transactions[1:]:
                    print(f"{row[0]:<10} {row[1]:<15} {row[2]:<15} {row[4]:<10}")
                print("-" * 50)
                input("\nPress Enter to return to the history menu...")

            elif choice == "2":
                while True:
                    clear_screen()
                    # Show list of all bills before selecting one
                    print("---- Available Bills ----")
                    print("{:<10} {:<15} {:<15} {:<10}".format("Bill No", "Date", "Time", "Total Amount"))
                    print("-" * 50)
                    for row in transactions[1:]:
                        print(f"{row[0]:<10} {row[1]:<15} {row[2]:<15} {row[4]:<10}")
                    print("-" * 50)

                    bill_no = input("Enter the Bill No to view full details (or type 'exit' to go back): ").strip()
                    if bill_no.lower() == "exit":
                        break

                    # Display details of the selected bill
                    for row in transactions[1:]:
                        if row[0] == bill_no:
                            clear_screen()
                            print(f"---- Detailed Bill for Bill No. {row[0]} ----")
                            print(f"Date: {row[1]}")
                            print(f"Time: {row[2]}")
                            print(f"Transaction Type: {row[3]}")
                            print("\n--- Purchased Items ---")

                            details = eval(row[5])  # Convert string representation of list to actual list
                            subtotal = 0
                            total_cgst = 0
                            total_sgst = 0

                            for idx, item in enumerate(details, start=1):
                                product_total = item['Price'] * item['Quantity']
                                item_cgst = product_total * cgst_rate / 100
                                item_sgst = product_total * sgst_rate / 100
                                subtotal += product_total
                                total_cgst += item_cgst
                                total_sgst += item_sgst

                                print(f"{idx}. {item['Item']} | Price: {item['Price']:.2f} | Quantity: {item['Quantity']}")
                                print(f"   Product price x quantity: {item['Price']} x {item['Quantity']} = {product_total:.2f}")
                                print(f"   GST (CGST + SGST): {item_cgst:.2f} + {item_sgst:.2f} = {item_cgst + item_sgst:.2f}")
                                print(f"   Total (with GST): {product_total + item_cgst + item_sgst:.2f}\n")

                            grand_total = subtotal + total_cgst + total_sgst

                            print("--- Bill Summary ---")
                            print(f"Subtotal: {subtotal:.2f}")
                            print(f"CGST ({cgst_rate}%): {total_cgst:.2f}")
                            print(f"SGST ({sgst_rate}%): {total_sgst:.2f}")
                            print(f"Grand Total: {grand_total:.2f}")

                            input("\nPress Enter to return to the history menu...")
                            break
                    else:
                        print("Bill No not found. Please try again.")
                        input("Press Enter to continue...")
            elif choice == "3":
                break
            else:
                print("Invalid option. Please try again.")

# Update CGST Rate
def update_cgst_rate():
    global cgst_rate
    try:
        cgst_rate = float(input(f"Enter new CGST rate (current: {cgst_rate}%): ").strip())
        print("CGST rate updated successfully.")
    except ValueError:
        print("Invalid rate. No changes made.")
    input("Press Enter to return to the admin dashboard...")

# Update SGST Rate
def update_sgst_rate():
    global sgst_rate
    try:
        sgst_rate = float(input(f"Enter new SGST rate (current: {sgst_rate}%): ").strip())
        print("SGST rate updated successfully.")
    except ValueError:
        print("Invalid rate. No changes made.")
    input("Press Enter to return to the admin dashboard...")

# Global variables for CGST and SGST rates
cgst_rate = 6.0
sgst_rate = 6.0

# Main execution
if __name__ == "__main__":
    initialize_files()
    main_menu()

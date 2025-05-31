import csv
from datetime import datetime
from csv import DictReader

LOG_FILENAME = "errorlog.txt"

def errorlogger(err):
    with open(LOG_FILENAME, "a") as e:
        e.write(err + "\n")
def load_transactions(transactions, filename):
    """Load transactions from a CSV file into a list of dictionaries."""
    transactions.clear()
    try:

        with open(filename, 'r') as csvfile:
            dict_reader = DictReader(csvfile)

            for row in dict_reader:

                try:
                    transaction_id = int(row['transaction_id'])
                    date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                    customer_id = int(row['customer_id'])
                    amount = float(row['amount'])
                    type = row['type'].strip().lower()
                    description = row['description'].strip()

                    if(type == 'debit'):
                        amount = -amount

                    transaction = {'transaction_id': transaction_id, 'date': date, 'customer_id': customer_id, 'amount': amount, 'type': type, 'description': description}

                    transactions.append(transaction)

                except ValueError as error:
                    print(f"Invalid row, skipping: {error}")
                    errorlogger(f"Invalid row, error: {error}")
        csvfile.close()

    except FileNotFoundError:
        print("File not found")
        errorlogger("File not found")
    
    print(f"loaded {len(transactions)} transactions")    
    return transactions
def view_transactions(transactions):
    headers = ['ID', 'Date', 'CustomerID', 'Amount', 'Type', 'Description']
    
    print("{:<6} | {:<12} | {:<12} | {:>15} | {:<10} | {}".format(*headers))
    print("-" * 100)

    for transaction in transactions:
        print("{:<6} | {:<12} | {:<12} | {:>15} | {:<10} | {}".format(
            transaction['transaction_id'],
            transaction['date'].strftime('%Y-%m-%d'),
            transaction['customer_id'],
            transaction['amount'],
            transaction['type'],
            transaction['description']
        ))
def create_transaction(transactions):
    try:
        transaction_id = max(transaction["transaction_id"] for transaction in transactions)+1
        date = input("Enter date of new transaction in YYYY-MM-DD format: ")
        date = datetime.strptime(date, "%Y-%m-%d").date()
        
        customer_id = int(input("Enter customer ID: "))
        
        type = input("Enter type (credit, debit, or transfer): ").lower()
        if type not in ['credit', 'debit', 'transfer']:
            print("Invalid transaction type")
            return

        amount = float(input("Enter the amount: "))

        if type == "debit":
            amount = abs(amount)

        description = input("Enter description: ")

        transaction = {'transaction_id': transaction_id, 'date': date, 'customer_id': customer_id, 'amount': amount, 'type': type, 'description': description}

        transactions.append(transaction)
        print("Success!")

    except ValueError as err:
        print(f"Input error: {err}")
def update_transaction(transactions):
    try:
        view_transactions(transactions)
        transaction_id = int(input("Enter the transaction ID you wish to change: "))
        field = input("Change which field? (amount, type, or description): ").strip().lower()
        
        for transaction in transactions:
            if transaction['transaction_id'] == transaction_id:
                if field in transaction:
                    new_value = input(f"Enter new value for '{field}': ")
                    transaction[field] = new_value
                    print("Updated!")
                    return
                else:
                    print(f"Field '{field}' not found.")
                    return

    except ValueError as err:
        print(f"Input error: {err}")
def delete_transaction(transactions):
    try:
        view_transactions(transactions)
        transaction_id = int(input("Enter the transaction ID you wish to delete"))

        for transaction in transactions:
            if transaction['transaction_id'] == transaction_id:
                print(transaction)
                confirm = input("Is this the correct transaction to delete? y or n").strip().lower()
                if confirm == "y":
                    transactions.remove(transaction)
                    print("Deleted transaction")
                    return
                elif confirm == "n":
                    print("Returning to menu")
                    return
                else:
                    print("Invalid input")
                    return
        print("Transaction not found")

    except ValueError as err:
        print(f"Input error: {err}")
def analyze_finances(transactions):
    try:
        total = {}
        print("Financial Summary:")

        for transaction in transactions:
            type = transaction["type"]
            amount = transaction["amount"]

            if type in total:
                total[type] += amount
            else:
                total[type] = amount

        for t in total:
            print(f"Total {t}: ${total[t]:.2f}")
            
        net = sum(t["amount"] for t in transactions)

        try:
            net -= total["transfer"]
        except:
            pass


        print(f"Net balance: ${net:.2f}")

    except ValueError as err:
        print(f"value error: {err}")
def save_transactions(transactions, filename):
    try:
        with open(filename, "w", newline="") as file:
            fieldnames = ['transaction_id', 'date', 'customer_id', 'amount', 'type', 'description']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader() 

            for transaction in transactions:
                if transaction['type'] == "debit":
                    transaction['amount'] = abs(transaction['amount'])
            writer.writerows(transactions)
    except ValueError as err:
        print("Failed to save transaction")

    print("Transactions saved.")
def generate_report(transactions):
    try:
        with open("report.txt", "w") as file:
            total = {}

            for transaction in transactions:
                type = transaction["type"]
                amount = transaction["amount"]

                if type in total:
                    total[type] += amount
                else:
                    total[type] = amount

            for t in total:
                file.write(f"Total {t}: ${total[t]:.2f}\n")
                
            net = sum(t["amount"] for t in transactions)

            try:
                net -= total["transfer"]
            except:
                pass
            file.write(f"Net balance: ${net:.2f}\n")

    except ValueError as err:
        print(f"value error: {err}")
def main():
    transactions = []

    choice = 1
    while(choice != "9"):
        print("1. Load Transactions\n2. Add Transaction\n3. View Transactions\n4. Update transaction\n5. Delete Transaction\n6. Analyze Finances\n7. Save Transactions\n8. Generate Report\n9. Exit")
        choice = input("Select an option: ").strip()
        filename = 'financial_transactions.csv'

        if(choice == "9"):
            print("Exiting program")
        elif(choice == "1"):
            load_transactions(transactions, filename)            
        elif(choice == "2"):
            create_transaction(transactions)
        elif(choice == "3"):
            view_transactions(transactions)        
        elif(choice == "4"):
            update_transaction(transactions)
        elif(choice == "5"):
            delete_transaction(transactions)
        elif(choice == "6"):
            analyze_finances(transactions)
        elif(choice == "7"):
            save_transactions(transactions, filename)
        elif(choice == "8"):
            generate_report(transactions)                        
        else:
            print("Invalid entry")

main()



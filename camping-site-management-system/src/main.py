import mysql.connector
from datetime import datetime

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Camping_site_Management_System',
}


def connect_db():
    return mysql.connector.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        database=DATABASE_CONFIG['database']
    )

def show_table(table_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

def insert_into(table_name, columns, values):
    conn = connect_db()
    cursor = conn.cursor()
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    print("Inserted successfully.\n")

def update_table(table_name, set_clause, condition_clause, values):
    conn = connect_db()
    cursor = conn.cursor()
    query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_clause}"
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    print("Updated successfully.\n")

def delete_from_table(table_name, condition_column, value):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE {condition_column} = %s", (value,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Deleted successfully.\n")

def menu():
    tables = {
        "1": "visitors",
        "2": "bookings",
        "3": "equipment",
        "4": "rentals",
        "5": "activities",
        "6": "activity_registration",
        "7": "staff"
    }

    while True:
        print("\n===== Camping Site Management Menu =====")
        print("1. Visitors")
        print("2. Bookings")
        print("3. Equipment")
        print("4. Rentals")
        print("5. Activities")
        print("6. Activity Registration")
        print("7. Staff")
        print("8. Exit")

        table_choice = input("Select a table to manage (1-8): ")

        if table_choice == "8":
            print("Exiting...")
            break
        elif table_choice not in tables:
            print("Invalid option. Try again.")
            continue

        table_name = tables[table_choice]

        print(f"\n--- {table_name.upper()} Menu ---")
        print("1. Show records")
        print("2. Add record")
        print("3. Modify record")
        print("4. Delete record")

        action = input("Select an action (1-4): ")

        if action == "1":
            show_table(table_name)

        elif action == "2":
            if table_name == "visitors":
                name = input("Name: ")
                contact = input("Contact (10 digits): ")
                email = input("Email: ")
                id_number = input("ID Number: ")
                insert_into(table_name, ['name', 'contact', 'email', 'id_number'],
                            [name, contact, email, id_number])

            elif table_name == "bookings":
                visitor_id = input("Visitor ID: ")
                campground_id = input("Campground ID: ")
                check_in = input("Check-in date (YYYY-MM-DD): ")
                check_out = input("Check-out date (YYYY-MM-DD): ")
                insert_into(table_name, ['visitor_id', 'campground_id', 'check_in', 'check_out'],
                            [visitor_id, campground_id, check_in, check_out])

            elif table_name == "equipment":
                name = input("Name: ")
                type_ = input("Type: ")
                price = input("Price: ")
                quantity = input("Quantity: ")
                condition = input("Condition: ")
                is_available = input("Is Available (1 for True, 0 for False): ")
                insert_into(table_name, ['name', 'type', 'price', 'quantity', 'equipment_condition', 'is_available'],
                            [name, type_, price, quantity, condition, is_available])

            elif table_name == "rentals":
                visitor_id = input("Visitor ID: ")
                equipment_id = input("Equipment ID: ")
                rental_date = input("Rental Date (YYYY-MM-DD): ")
                return_date = input("Return Date (YYYY-MM-DD): ")
                insert_into(table_name, ['visitor_id', 'equipment_id', 'rental_date', 'return_date'],
                            [visitor_id, equipment_id, rental_date, return_date])

            elif table_name == "activities":
                name = input("Activity Name: ")
                date = input("Date (YYYY-MM-DD): ")
                max_participants = input("Max Participants: ")
                price = input("Price: ")
                insert_into(table_name, ['name', 'date', 'max_participants', 'price'],
                            [name, date, max_participants, price])

            elif table_name == "activity_registration":
                activity_id = input("Activity ID: ")
                visitor_id = input("Visitor ID: ")
                insert_into(table_name, ['activity_id', 'visitor_id'],
                            [activity_id, visitor_id])

            elif table_name == "staff":
                name = input("Name: ")
                department = input("Department: ")
                designation = input("Designation: ")
                hod = input("HOD: ")
                contact = input("Contact: ")
                email = input("Email: ")
                address = input("Address: ")
                salary = input("Salary: ")
                insert_into(table_name, ['name', 'department', 'designation', 'HOD', 'contact', 'email', 'address', 'salary'],
                            [name, department, designation, hod, contact, email, address, salary])

        elif action == "3":
            id_col = input("Enter ID column name (e.g., visitor_id): ")
            id_val = input(f"Enter ID value to update in {table_name}: ")
            set_clause = input("Enter SET clause (e.g., name = %s, contact = %s): ")
            values_raw = input("Enter new values (comma-separated): ")
            values = [v.strip() for v in values_raw.split(',')]
            values.append(id_val)
            update_table(table_name, set_clause, f"{id_col} = %s", values)

        elif action == "4":
            id_col = input("Enter ID column name (e.g., visitor_id): ")
            id_val = input(f"Enter ID value to delete from {table_name}: ")
            delete_from_table(table_name, id_col, id_val)

        else:
            print("Invalid action. Try again.")

if __name__ == "__main__":
    menu()

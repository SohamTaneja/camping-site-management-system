import mysql.connector
import tabulate

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Camping_site_Management_System',
}

def get_connection():
    return mysql.connector.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        database=DATABASE_CONFIG['database']
    )

def insert_sample_data():
    conn = get_connection()
    cursor = conn.cursor()
    # Sample Visitors
    cursor.execute("INSERT INTO visitors (name, contact, id_number) VALUES ('Alice', '1234567890', 'ID001')")
    cursor.execute("INSERT INTO visitors (name, contact, id_number) VALUES ('Bob', '0987654321', 'ID002')")
    # Sample Campgrounds
    cursor.execute("INSERT INTO campgrounds (name, type, capacity) VALUES ('Pine Tent', 'Tent', 2)")
    cursor.execute("INSERT INTO campgrounds (name, type, capacity) VALUES ('Oak Cabin', 'Cabin', 4)")
    # Sample Equipment
    cursor.execute("INSERT INTO equipment (name, type, equipment_condition) VALUES ('Kayak', 'Boat', 'Good')")
    cursor.execute("INSERT INTO equipment (name, type, equipment_condition) VALUES ('Tent', 'Shelter', 'Good')")
    # Sample Activities
    cursor.execute("INSERT INTO activities (name, date, max_participants) VALUES ('Kayaking', '2025-06-01', 10)")
    cursor.execute("INSERT INTO activities (name, date, max_participants) VALUES ('Hiking', '2025-06-02', 15)")
    conn.commit()
    cursor.close()
    conn.close()
    print("Sample data inserted.")

def add_visitor():
    name = input("Name: ")
    contact = input("Contact: ")
    id_number = input("ID Number: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO visitors (name, contact, id_number) VALUES (%s, %s, %s)", (name, contact, id_number))
    conn.commit()
    cursor.close()
    conn.close()
    print("Visitor added.")

def update_visitor():
    visitor_id = input("Visitor ID to update: ")
    name = input("New Name: ")
    contact = input("New Contact: ")
    id_number = input("New ID Number: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE visitors SET name=%s, contact=%s, id_number=%s WHERE visitor_id=%s", (name, contact, id_number, visitor_id))
    conn.commit()
    cursor.close()
    conn.close()
    print("Visitor updated.")

def delete_visitor():
    visitor_id = input("Visitor ID to delete: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM visitors WHERE visitor_id=%s", (visitor_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Visitor deleted.")

def show_visitors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT visitor_id, name, contact, id_number FROM visitors")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if rows:
        print(tabulate.tabulate(rows, headers=["ID", "Name", "Contact", "ID Number"], tablefmt="grid"))
    else:
        print("No visitors found.")

def show_available_campgrounds():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT campground_id, name, type, capacity FROM campgrounds WHERE status='available'")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if rows:
        print(tabulate.tabulate(rows, headers=["Campground ID", "Name", "Type", "Capacity"], tablefmt="grid"))
    else:
        print("No available campgrounds.")

def check_in():
    visitor_id = input("Visitor ID: ")
    show_available_campgrounds()
    campground_id = input("Campground ID to book: ")
    check_in_date = input("Check-in date (YYYY-MM-DD): ")
    check_out_date = input("Check-out date (YYYY-MM-DD): ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (visitor_id, campground_id, check_in, check_out) VALUES (%s, %s, %s, %s)",
        (visitor_id, campground_id, check_in_date, check_out_date)
    )
    cursor.execute(
        "UPDATE campgrounds SET status='booked' WHERE campground_id=%s", (campground_id,)
    )
    # Log check-in
    cursor.execute(
        "INSERT INTO checkins (visitor_id, check_in_time) VALUES (%s, NOW())", (visitor_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("Check-in complete.")

def check_out():
    booking_id = input("Booking ID to check out: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT visitor_id, campground_id FROM bookings WHERE booking_id=%s", (booking_id,))
    result = cursor.fetchone()
    if result:
        visitor_id, campground_id = result
        cursor.execute("UPDATE campgrounds SET status='available' WHERE campground_id=%s", (campground_id,))
        cursor.execute("DELETE FROM bookings WHERE booking_id=%s", (booking_id,))
        # Log check-out
        cursor.execute("UPDATE checkins SET check_out_time=NOW() WHERE visitor_id=%s AND check_out_time IS NULL", (visitor_id,))
        conn.commit()
        print("Check-out complete.")
    else:
        print("Booking not found.")
    cursor.close()
    conn.close()

def report_equipment_damage():
    equipment_id = input("Equipment ID: ")
    description = input("Damage description: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE equipment SET equipment_condition='Damaged', is_available=FALSE WHERE equipment_id=%s",
        (equipment_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("Damage reported.")

def show_equipment():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT equipment_id, name, type, equipment_condition, is_available FROM equipment")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if rows:
        print(tabulate.tabulate(rows, headers=["ID", "Name", "Type", "Condition", "Available"], tablefmt="grid"))
    else:
        print("No equipment found.")

def rent_equipment():
    visitor_id = input("Visitor ID: ")
    show_equipment()
    equipment_id = input("Equipment ID to rent: ")
    rental_date = input("Rental date (YYYY-MM-DD): ")
    return_date = input("Return date (YYYY-MM-DD): ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO rentals (visitor_id, equipment_id, rental_date, return_date) VALUES (%s, %s, %s, %s)",
        (visitor_id, equipment_id, rental_date, return_date)
    )
    cursor.execute(
        "UPDATE equipment SET is_available=FALSE WHERE equipment_id=%s", (equipment_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("Equipment rented.")

def show_activities():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT activity_id, name, date, max_participants FROM activities")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if rows:
        print(tabulate.tabulate(rows, headers=["Activity ID", "Name", "Date", "Max Participants"], tablefmt="grid"))
    else:
        print("No activities found.")

def register_activity():
    visitor_id = input("Visitor ID: ")
    show_activities()
    activity_id = input("Activity ID to register for: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO activity_registration (activity_id, visitor_id) VALUES (%s, %s)",
        (activity_id, visitor_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("Activity registration complete.")

def menu():
    while True:
        print("\n--- Camping Site Management ---")
        print("1. Add Visitor")
        print("2. Update Visitor")
        print("3. Delete Visitor")
        print("4. Insert Sample Data")
        print("5. Show Visitors")
        print("6. Show Available Campgrounds")
        print("7. Check-in")
        print("8. Check-out")
        print("9. Show Equipment")
        print("10. Report Equipment Damage")
        print("11. Rent Equipment")
        print("12. Show Activities")
        print("13. Register for Activity")
        print("14. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            add_visitor()
        elif choice == '2':
            update_visitor()
        elif choice == '3':
            delete_visitor()
        elif choice == '4':
            insert_sample_data()
        elif choice == '5':
            show_visitors()
        elif choice == '6':
            show_available_campgrounds()
        elif choice == '7':
            check_in()
        elif choice == '8':
            check_out()
        elif choice == '9':
            show_equipment()
        elif choice == '10':
            report_equipment_damage()
        elif choice == '11':
            rent_equipment()
        elif choice == '12':
            show_activities()
        elif choice == '13':
            register_activity()
        elif choice == '14':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    print("Welcome to Camping Site Management System")
    menu()

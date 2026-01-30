
import mysql.connector
from datetime import datetime, timedelta
from tabulate import tabulate
import calendar
from decimal import Decimal

def connect_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="Camping_Management")

def to_float(val):
    """Convert Decimal to float safely"""
    return float(val) if isinstance(val, Decimal) else val

# ==================== AUTHENTICATION ====================

def login():
    db = connect_db()
    cur = db.cursor()
    u = input("Username: ")
    p = input("Password: ")
    cur.execute("SELECT user_id, role, name FROM users WHERE username=%s AND password=%s", (u, p))
    result = cur.fetchone()
    cur.close()
    db.close()
   
    if result:
        user_id, role, name = result
        print(f"✓ Login successful! Welcome {name}")
        return user_id, role
    print("❌ Login failed.")
    return None, None

def signup():
    db = connect_db()
    cur = db.cursor()
    u = input("Username: ")
   
    # Check if username exists
    cur.execute("SELECT user_id FROM users WHERE username=%s", (u,))
    if cur.fetchone():
        print("❌ Username already exists.")
        cur.close()
        db.close()
        return
   
    p = input("Password: ")
    p_confirm = input("Confirm Password: ")
   
    if p != p_confirm:
        print("❌ Passwords don't match!")
        cur.close()
        db.close()
        return
   
    name = input("Name: ")
    contact = input("Contact: ")
    email = input("Email: ")
   
    cur.execute(
        "INSERT INTO users (username, password, role, name, contact, email) VALUES (%s,%s,'customer',%s,%s,%s)",
        (u, p, name, contact, email)
    )
    db.commit()
    print("✓ Account created!")
    cur.close()
    db.close()

# ==================== CALENDAR WITH COLORS ====================

def show_calendar_availability():
    """Display calendar with booked dates in RED, available in GREEN"""
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT check_in, check_out FROM bookings WHERE status='confirmed'")
    bookings = cur.fetchall()
    cur.close()
    db.close()

    booked_dates = set()
    for ci, co in bookings:
        if ci and co:
            d = ci
            while d <= co:
                booked_dates.add(d)
                d += timedelta(days=1)

    today = datetime.today()
    year, month = today.year, today.month
    cal = calendar.TextCalendar().formatmonth(year, month)
    print("\n" + f"Calendar for {calendar.month_name[month]} {year}")
    for line in cal.splitlines():
        for w in line.split():
            if w.isdigit():
                try:
                    d = datetime(year, month, int(w)).date()
                    if d in booked_dates:
                        print("\033[91m" + w.rjust(3) + "\033[0m", end=" ")
                    else:
                        print("\033[92m" + w.rjust(3) + "\033[0m", end=" ")
                except:
                    print(w.rjust(3), end=" ")
            else:
                print(w, end=" ")
        print()


def get_date_input(prompt="Enter date (YYYY-MM-DD): "):
    """Validate date input"""
    while True:
        try:
            date_str = input(prompt)
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj < datetime.now().date():
                print("❌ Please select a future date.")
                continue
            return date_obj
        except ValueError:
            print("❌ Invalid format. Use YYYY-MM-DD.")

# ==================== CUSTOMER FUNCTIONS ====================

def show_table(table, user_id=None):
    """Display table with proper formatting"""
    db = connect_db()
    cur = db.cursor()
   
    if table == "bookings" and user_id:
        cur.execute("SELECT booking_id, campground_name, check_in, check_out, selling_price, status FROM bookings WHERE user_id=%s", (user_id,))
    elif table == "activities":
        # Hide cost_price and date from customers, show only activity_id, name, and selling_price
        cur.execute("SELECT activity_id, activity_name, selling_price FROM activities")
    else:
        cur.execute(f"SELECT * FROM {table}")
   
    rows = cur.fetchall()
    headers = [desc[0] for desc in cur.description]
   
    # Convert Decimal values
    rows = [[to_float(cell) if isinstance(cell, Decimal) else cell for cell in row] for row in rows]
   
    print(tabulate(rows, headers, tablefmt="grid"))
    cur.close()
    db.close()
def book_activity(user_id):
    """Book activity with optional equipment rental"""
    show_calendar_availability()
    show_table("activities")
   
    try:
        activity_id = int(input("Activity ID: "))
        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT activity_name, selling_price FROM activities WHERE activity_id=%s", (activity_id,))
        result = cur.fetchone()
       
        if not result:
            print("❌ Activity not found.")
            cur.close()
            db.close()
            return
       
        activity_name, price = result
        price = to_float(price)
       
        check_in = get_date_input("Check-in (YYYY-MM-DD): ")
        check_out = get_date_input("Check-out (YYYY-MM-DD): ")
       
        if check_out <= check_in:
            print("❌ Check-out must be after check-in.")
            cur.close()
            db.close()
            return
       
        days = (check_out - check_in).days
        total_activity = price * days
       
        # Equipment rental
        rental_cost = 0
        rental_id = None
        rent_choice = input("Rent equipment? (yes/no): ").lower()
        if rent_choice == "yes":
            rental_id, rental_cost = rent_equipment(user_id, activity_id, check_in, check_out)
       
        rental_cost = to_float(rental_cost) if rental_cost else 0
        grand_total = total_activity + rental_cost
       
        # Receipt
        print("\n" + "="*70)
        print("RECEIPT")
        print("="*70)
        print(f"Activity: {activity_name:30} ${total_activity:.2f}")
        if rental_id:
            print(f"Equipment Rental (ID:{rental_id}): {rental_cost:20.2f}")
        else:
            print(f"Equipment Rental: {'Not Selected':20} $0.00")
        print("-"*70)
        print(f"TOTAL: ${grand_total:.2f}")
        print("="*70)
       
        if input("Proceed to checkout? (yes/no): ").lower() == "yes":
            cur.execute(
                "INSERT INTO bookings (user_id, campground_name, check_in, check_out, selling_price, status) VALUES (%s,%s,%s,%s,%s,'confirmed')",
                (user_id, activity_name, check_in, check_out, grand_total)
            )
            db.commit()
            print("✓ Booking confirmed!")
        else:
            print("❌ Checkout cancelled.")
       
        cur.close()
        db.close()
    except ValueError:
        print("❌ Invalid input.")

def rent_equipment(user_id, activity_id, check_in, check_out):
    """Rent equipment for activity"""
    db = connect_db()
    cur = db.cursor()
   
    cur.execute("SELECT equipment_id, name, price FROM equipment WHERE is_available=1")
    equipment = cur.fetchall()
   
    if not equipment:
        print("No equipment available.")
        cur.close()
        db.close()
        return None, 0
   
    print("\n" + "="*60)
    print("AVAILABLE EQUIPMENT")
    print("="*60)
    for equip in equipment:
        equip_id, name, price = equip
        price = to_float(price)
        print(f"ID: {equip_id} | {name:20} | ${price}/day")
    print("="*60)
   
    try:
        equip_id = int(input("Equipment ID: "))
        equip = next((e for e in equipment if e[0] == equip_id), None)
       
        if not equip:
            print("❌ Equipment not found.")
            cur.close()
            db.close()
            return None, 0
       
        price_per_day = to_float(equip[2])
        rental_days = (check_out - check_in).days
        total_cost = rental_days * price_per_day
       
        cur.execute(
            "INSERT INTO rentals (user_id, activity_id, equipment_id, start_date, end_date, total_cost, rental_status) VALUES (%s,%s,%s,%s,%s,%s,'confirmed')",
            (user_id, activity_id, equip_id, check_in, check_out, total_cost)
        )
        db.commit()
        rental_id = cur.lastrowid
        print(f"✓ Equipment rented! Days: {rental_days}, Cost: ${total_cost:.2f}")
       
        cur.close()
        db.close()
        return rental_id, total_cost
    except ValueError:
        print("❌ Invalid input.")
        cur.close()
        db.close()
        return None, 0

def modify_booking(user_id):
    """Modify booking or rental dates"""
    show_table("bookings", user_id)
   
    try:
        booking_id = int(input("Booking ID to modify: "))
        db = connect_db()
        cur = db.cursor()
       
        cur.execute("SELECT * FROM bookings WHERE booking_id=%s AND user_id=%s", (booking_id, user_id))
        if not cur.fetchone():
            print("❌ Booking not found.")
            cur.close()
            db.close()
            return
       
        print("1. Change Check-in  2. Change Check-out  3. Change Both")
        choice = input("Choice: ")
       
        if choice == "1":
            new_date = get_date_input("New check-in: ")
            cur.execute("UPDATE bookings SET check_in=%s WHERE booking_id=%s", (new_date, booking_id))
        elif choice == "2":
            new_date = get_date_input("New check-out: ")
            cur.execute("UPDATE bookings SET check_out=%s WHERE booking_id=%s", (new_date, booking_id))
        elif choice == "3":
            ci = get_date_input("New check-in: ")
            co = get_date_input("New check-out: ")
            if co <= ci:
                print("❌ Invalid dates.")
                cur.close()
                db.close()
                return
            cur.execute("UPDATE bookings SET check_in=%s, check_out=%s WHERE booking_id=%s", (ci, co, booking_id))
       
        db.commit()
        print("✓ Updated!")
        cur.close()
        db.close()
    except ValueError:
        print("❌ Invalid input.")

def cancel_booking(user_id):
    """Cancel booking and get 50% refund"""
    show_table("bookings", user_id)
   
    try:
        booking_id = int(input("Booking ID to cancel: "))
        db = connect_db()
        cur = db.cursor()
       
        cur.execute("SELECT selling_price FROM bookings WHERE booking_id=%s AND user_id=%s AND status='confirmed'", (booking_id, user_id))
        result = cur.fetchone()
       
        if not result:
            print("❌ Booking not found or not confirmed.")
            cur.close()
            db.close()
            return
       
        original_price = to_float(result[0])
        refund = original_price * 0.5
       
        print(f"Original: ${original_price:.2f}")
        print(f"Refund (50%): ${refund:.2f}")
       
        if input("Confirm cancellation? (yes/no): ").lower() == "yes":
            cur.execute("UPDATE bookings SET status='cancelled' WHERE booking_id=%s", (booking_id,))
            db.commit()
            print(f"✓ Cancelled! Refund: ${refund:.2f}")
       
        cur.close()
        db.close()
    except ValueError:
        print("❌ Invalid input.")

# ==================== ADMIN FUNCTIONS ====================

def add_record(table):
    db = connect_db()
    cur = db.cursor()
   
    if table == "activities":
        name = input("Activity name: ")
        price = float(input("Price: "))
        cost = float(input("Cost: "))
        date = input("Date (YYYY-MM-DD): ")
        cur.execute("INSERT INTO activities (activity_name, selling_price, cost_price, date, user_id) VALUES (%s,%s,%s,%s,1)",
                   (name, price, cost, date))
    elif table == "equipment":
        name = input("Equipment name: ")
        price = float(input("Price: "))
        qty = int(input("Quantity: "))
        cur.execute("INSERT INTO equipment (name, price, quantity, is_available) VALUES (%s,%s,%s,1)", (name, price, qty))
    elif table == "users":
        u = input("Username: ")
        p = input("Password: ")
        role = input("Role (admin/customer): ")
        name = input("Name: ")
        contact = input("Contact: ")
        email = input("Email: ")
        cur.execute("INSERT INTO users (username, password, role, name, contact, email) VALUES (%s,%s,%s,%s,%s,%s)",
                   (u, p, role, name, contact, email))
   
    db.commit()
    print("✓ Added!")
    cur.close()
    db.close()

def modify_record(table):
    db = connect_db()
    cur = db.cursor()
   
    if table == "activities":
        aid = input("Activity ID: ")
        name = input("New name: ")
        price = float(input("New price: "))
        cost = float(input("New cost: "))
        cur.execute("UPDATE activities SET activity_name=%s, selling_price=%s, cost_price=%s WHERE activity_id=%s",
                   (name, price, cost, aid))
    elif table == "equipment":
        eid = input("Equipment ID: ")
        name = input("New name: ")
        price = float(input("New price: "))
        qty = int(input("New qty: "))
        cur.execute("UPDATE equipment SET name=%s, price=%s, quantity=%s WHERE equipment_id=%s",
                   (name, price, qty, eid))
    elif table == "users":
        uid = input("User ID: ")
        name = input("New name: ")
        contact = input("New contact: ")
        email = input("New email: ")
        cur.execute("UPDATE users SET name=%s, contact=%s, email=%s WHERE user_id=%s",
                   (name, contact, email, uid))
   
    db.commit()
    print("✓ Modified!")
    cur.close()
    db.close()

def delete_record(table):
    db = connect_db()
    cur = db.cursor()
   
    # Fix: Remove the 's' properly for singular form
    if table == "activities":
        table_id = "activity_id"
    elif table == "equipment":
        table_id = "equipment_id"
    elif table == "users":
        table_id = "user_id"
    else:
        table_id = f"{table[:-1]}_id"
   
    record_id = input(f"{table} ID: ")
   
    cur.execute(f"DELETE FROM {table} WHERE {table_id}=%s", (record_id,))
    db.commit()
    print("✓ Deleted!")
    cur.close()
    db.close()

def show_stats():
    """Show finance statistics"""
    db = connect_db()
    cur = db.cursor()
   
    cur.execute("SELECT COUNT(*), SUM(selling_price) FROM bookings WHERE status='confirmed'")
    count, total = cur.fetchone()
    total = to_float(total) if total else 0
   
    cur.execute("SELECT COUNT(*), SUM(total_cost) FROM rentals WHERE rental_status='confirmed'")
    rentals_count, rentals_total = cur.fetchone()
    rentals_total = to_float(rentals_total) if rentals_total else 0
   
    data = [
        ("Confirmed Bookings", count),
        ("Booking Revenue", f"${total:.2f}"),
        ("Equipment Rentals", rentals_count),
        ("Rental Revenue", f"${rentals_total:.2f}"),
        ("Total Revenue", f"${total + rentals_total:.2f}")
    ]
   
    print(tabulate(data, headers=["Metric", "Value"], tablefmt="grid"))
    cur.close()
    db.close()
# ==================== MAIN MENU ====================
def customer_menu(user_id):
    while True:
        print("\n1.Book Activity  2.My Bookings  3.Modify Dates  4.Cancel Booking  5.Logout")
        choice = input("Choice: ")
       
        if choice == "1":
            book_activity(user_id)
        elif choice == "2":
            show_table("bookings", user_id)
        elif choice == "3":
            modify_booking(user_id)
        elif choice == "4":
            cancel_booking(user_id)
        elif choice == "5":
            Break
def admin_menu():
    while True:
        print("\n1.Users  2.Bookings  3.Equipment  4.Activities  5.Rentals  6.Stats  7.Add  8.Modify  9.Delete  10.Logout")
        choice = input("Choice: ")
        if choice == "1":
            show_table("users")
        elif choice == "2":
            show_table("bookings")
        elif choice == "3":
            show_table("equipment")
        elif choice == "4":
            show_table("activities")
        elif choice == "5":
            show_table("rentals")
        elif choice == "6":
            show_stats()
        elif choice == "7":
            table = input("Table (activities/equipment/users): ")
            add_record(table)
        elif choice == "8":
            table = input("Table (activities/equipment/users): ")
            modify_record(table)
        elif choice == "9":
            table = input("Table (activities/equipment/users): ")
            delete_record(table)
        elif choice == "10":
            break

def main():
    while True:
        print("\n" + "="*40)
        print("CAMPING SITE MANAGEMENT SYSTEM")
        print("="*40)
        print("1.Login  2.Sign Up  3.Exit")
        choice = input("Choice: ")
       
        if choice == "1":
            user_id, role = login()
            if user_id:
                if role == "admin":
                    admin_menu()
                else:
                    customer_menu(user_id)
        elif choice == "2":
            signup()
        elif choice == "3":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()

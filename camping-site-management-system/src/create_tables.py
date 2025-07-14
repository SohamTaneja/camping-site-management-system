import mysql.connector
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Camping_site_Management_System'
}

def create_tables():
    # Connect without database to create it
    conn = mysql.connector.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password']
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Camping_site_Management_System")
    cursor.close()
    conn.close()

    # Reconnect with database (this is the correct way)
    conn = mysql.connector.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        database=DATABASE_CONFIG['database']  # Now specify the database
    )
    cursor = conn.cursor()

    # Visitors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitors (
        visitor_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        contact CHAR(10),
        email VARCHAR(100),
        id_number BIGINT
    )
    """)

    # Bookings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INT AUTO_INCREMENT PRIMARY KEY,
        visitor_id INT,
        campground_id INT,
        check_in DATE,
        check_out DATE,
        FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id)
    )
    """)

    # Equipment table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment (
        equipment_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        type VARCHAR(50),
        price DECIMAL(10, 2),
        quantity INT,
        equipment_condition VARCHAR(50),
        is_available BOOLEAN DEFAULT TRUE
    )
    """)

    # Rentals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rentals (
        rental_id INT AUTO_INCREMENT PRIMARY KEY,
        visitor_id INT,
        equipment_id INT,
        rental_date DATE,
        return_date DATE,
        FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id),
        FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
    )
    """)

    # Activities table (fixed comma)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        activity_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        date DATE,
        max_participants INT,
        price DECIMAL(10, 2)
    )
    """)

    # Activity Registration table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_registration (
        registration_id INT AUTO_INCREMENT PRIMARY KEY,
        activity_id INT,
        visitor_id INT,
        FOREIGN KEY (activity_id) REFERENCES activities(activity_id),
        FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id)
    )
    """)

    # Staff table (fixed comma)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        staff_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        department VARCHAR(50),
        designation VARCHAR(50),
        HOD VARCHAR(100),
        contact CHAR(10),
        email VARCHAR(100),
        address VARCHAR(255),
        salary DECIMAL(10, 2)
    )
    """)

        # Insert sample data only if not already inserted
    cursor.execute("SELECT COUNT(*) FROM visitors")
    if cursor.fetchone()[0] == 0:
        # Visitors
        cursor.execute("INSERT INTO visitors (name, contact, email, id_number) VALUES ('Alice', '1234567890', 'alice@example.com', 1001)")
        cursor.execute("INSERT INTO visitors (name, contact, email, id_number) VALUES ('Bob', '0987654321', 'bob@example.com', 1002)")

        # Equipment
        cursor.execute("INSERT INTO equipment (name, type, price, quantity, equipment_condition, is_available) VALUES ('Kayak', 'Boat', 100.0, 5, 'Good', TRUE)")
        cursor.execute("INSERT INTO equipment (name, type, price, quantity, equipment_condition, is_available) VALUES ('Tent', 'Shelter', 50.0, 10, 'Good', TRUE)")

        # Activities
        cursor.execute("INSERT INTO activities (name, date, max_participants, price) VALUES ('Kayaking', '2025-06-01', 10, 200.0)")
        cursor.execute("INSERT INTO activities (name, date, max_participants, price) VALUES ('Hiking', '2025-06-02', 15, 150.0)")

        # Bookings
        cursor.execute("INSERT INTO bookings (visitor_id, campground_id, check_in, check_out) VALUES (1, 101, '2025-07-01', '2025-07-05')")
        cursor.execute("INSERT INTO bookings (visitor_id, campground_id, check_in, check_out) VALUES (2, 102, '2025-07-02', '2025-07-06')")

        # Rentals
        cursor.execute("INSERT INTO rentals (visitor_id, equipment_id, rental_date, return_date) VALUES (1, 1, '2025-07-01', '2025-07-02')")
        cursor.execute("INSERT INTO rentals (visitor_id, equipment_id, rental_date, return_date) VALUES (2, 2, '2025-07-03', '2025-07-04')")

        # Activity Registration
        cursor.execute("INSERT INTO activity_registration (activity_id, visitor_id) VALUES (1, 1)")
        cursor.execute("INSERT INTO activity_registration (activity_id, visitor_id) VALUES (2, 2)")

        # Staff
        cursor.execute("INSERT INTO staff (name, department, designation, HOD, contact, email, address, salary) VALUES ('John Smith', 'Operations', 'Manager', 'Jane Doe', '1112223333', 'john@camp.com', '123 Forest Lane', 45000.00)")
        cursor.execute("INSERT INTO staff (name, department, designation, HOD, contact, email, address, salary) VALUES ('Emily Davis', 'Recreation', 'Guide', 'Jane Doe', '4445556666', 'emily@camp.com', '456 River Road', 32000.00)")

        print("Sample data inserted.")
    else:
        print("Sample data already exists. Skipping inserts.")

    conn.commit()
    cursor.close()
    conn.close()
    print("All tables created or updated successfully.")

if __name__ == "__main__":
    create_tables()

import mysql.connector
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Soham@123',
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
    
    conn.commit()
    cursor.close()
    conn.close()
    print("All tables created or updated successfully.")

if __name__ == "__main__":
    create_tables()

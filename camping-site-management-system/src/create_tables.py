import mysql.connector

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''
}

def create_database_and_tables():
    # Connect to MySQL server (no DB)
    conn = mysql.connector.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password']
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Camping_Management")
    cursor.close()
    conn.close()

    # Connect to your database
    conn = mysql.connector.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        database='Camping_Management'
    )
    cursor = conn.cursor()

    # Users table without salary
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role ENUM('admin','customer') NOT NULL,
        name VARCHAR(100),
        contact VARCHAR(15),
        email VARCHAR(100)
    );
    """)

    # Equipment table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment (
        equipment_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        price DECIMAL(10,2),
        quantity INT,
        is_available BOOLEAN DEFAULT TRUE
    );
    """)

    # Activities table without location
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        activity_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        activity_name VARCHAR(100),
        date DATE,
        cost_price DECIMAL(10,2),
        selling_price DECIMAL(10,2),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    # Bookings table without location
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        campground_name VARCHAR(100),
        check_in DATE,
        check_out DATE,
        equipment_ids VARCHAR(255),
        selling_price DECIMAL(10,2),
        status ENUM('confirmed','cancelled','completed') DEFAULT 'confirmed',
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rentals (
        rental_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        activity_id INT NOT NULL,
        equipment_id INT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        total_cost DECIMAL(10,2) NOT NULL,
        rental_status ENUM('pending','confirmed','completed','cancelled') DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (activity_id) REFERENCES activities(activity_id),
        FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
    );
    """)
    # Insert sample users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO users (username, password, role, name, contact, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, [
            ('admin1', 'adminpass', 'admin', 'Admin User', '9999999999', 'admin@example.com'),
            ('customer1', 'custpass', 'customer', 'John Doe', '8888888888', 'user@example.com')
        ])

    # Insert sample equipment
    cursor.execute("SELECT COUNT(*) FROM equipment")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO equipment (name, price, quantity, is_available)
        VALUES (%s, %s, %s, %s)
        """, [
            ('Tent', 50.0, 10, True),
            ('Sleeping Bag', 20.0, 15, True),
        ])
   
    # Insert sample activities
    cursor.execute("SELECT COUNT(*) FROM activities")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO activities (user_id, activity_name, date, cost_price, selling_price)
        VALUES (%s, %s, %s, %s, %s)
        """, [
            (1, 'Hiking', '2025-09-20', 50.0, 100.0),
            (1, 'Kayaking', '2025-09-22', 80.0, 150.0)
        ])

    # Insert sample bookings
    cursor.execute("SELECT COUNT(*) FROM bookings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO bookings (user_id, campground_name, check_in, check_out, equipment_ids, selling_price, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (2, 'Sunny Campground', '2025-09-20', '2025-09-22', None, 300.0, 'confirmed'))
    cursor.execute("SELECT COUNT(*) FROM rentals")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO rentals (user_id, activity_id, equipment_id, start_date, end_date, total_cost, rental_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, [
            (2, 1, 1, '2025-09-20', '2025-09-22', 100.0, 'confirmed'),
            (2, 2, 2, '2025-09-22', '2025-09-24', 40.0, 'confirmed')
        ])
    conn.commit()
    cursor.close()
    conn.close()
    print("Database and tables created, sample data inserted.")

if __name__ == "__main__":
    create_database_and_tables()

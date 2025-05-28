import mysql.connector

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Soham@123',
    'database': 'Camping_site_Management_System',
}

def create_tables():
    conn = mysql.connector.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password']
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Camping_site_Management_System")
    conn.database = DATABASE_CONFIG['database']

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitors (
        visitor_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        contact VARCHAR(50),
        id_number VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS campgrounds (
        campground_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        type VARCHAR(50),
        capacity INT,
        status ENUM('available', 'booked') DEFAULT 'available'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INT AUTO_INCREMENT PRIMARY KEY,
        visitor_id INT,
        campground_id INT,
        check_in DATE,
        check_out DATE,
        FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id),
        FOREIGN KEY (campground_id) REFERENCES campgrounds(campground_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment (
        equipment_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        type VARCHAR(50),
        equipment_condition VARCHAR(50),
        is_available BOOLEAN DEFAULT TRUE
    )
    """)

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        activity_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        date DATE,
        max_participants INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_registration (
        registration_id INT AUTO_INCREMENT PRIMARY KEY,
        activity_id INT,
        visitor_id INT,
        FOREIGN KEY (activity_id) REFERENCES activities(activity_id),
        FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checkins (
        checkin_id INT AUTO_INCREMENT PRIMARY KEY,
        visitor_id INT,
        check_in_time DATETIME,
        check_out_time DATETIME,
        FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        staff_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        role VARCHAR(50)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("All tables created successfully.")

if __name__ == "__main__":
    create_tables()
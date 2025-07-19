import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import Error
import os
from dotenv import load_dotenv

def connect_to_database():
    """Connect to database"""
    load_dotenv()
    try:
        conn = psycopg2.connect(host = os.getenv("HOST"), dbname = os.getenv("DBNAME"), user = os.getenv("USER"), password = os.getenv("PASSWORD"), port = os.getenv("PORT"))
        return conn    
    except Error as e:
        print(f"Error connecting to database: {e}")
        

def create_table(conn):
    """Create a table"""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS no_frills_db_test_1(
                            product_id VARCHAR(255) PRIMARY KEY,
                            product_name VARCHAR(255),
                            package_size VARCHAR(255),
                            current_price VARCHAR(10),
                            previous_price VARCHAR(10)
                        );
                        """)
        conn.commit()
    except Error as e:
        print(f"Error creating table: {e}")
        
def insert_data(conn, data):
    """Insert into table, data must by in a list of tuple for execute_values to work"""
    try:
        with conn.cursor() as cur:
            query = """
            INSERT INTO no_frills_db_test_1 (product_id, product_name, package_size, current_price, previous_price) VALUES %s
            ON CONFLICT(product_id)
            DO UPDATE SET
                product_name = EXCLUDED.product_name,
                package_size = EXCLUDED.package_size,
                current_price = EXCLUDED.current_price,
                previous_price = EXCLUDED.previous_price;
            """
            execute_values(cur, query, data)
            conn.commit()
    except Error as e:
        print(f"Error inserting to table: {e}")


def save_scraped_data(data):
    conn = connect_to_database()
    if conn:
        try:
            create_table(conn)
            insert_data(conn,data)
        finally:
            conn.close()
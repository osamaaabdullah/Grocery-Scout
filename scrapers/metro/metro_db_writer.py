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


"""Functions to store scraped data"""     
   
def create_table(conn,storeid):
    """Create a table"""
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                        CREATE TABLE IF NOT EXISTS metro_db_{storeid}(
                            product_id      VARCHAR(100) PRIMARY KEY,
                            product_name    VARCHAR(255),
                            package_size    VARCHAR(255),
                            current_price   VARCHAR(20),
                            previous_price  VARCHAR(20)
                        );
                        """)
        conn.commit()
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(conn, data,store_id):
    """Insert into table, data must by in a list of tuple for execute_values to work"""
    try:
        # seen = {}
        # for item in data:
        #     product_id = item[0]
        #     seen[product_id] = item  # last one wins if duplicates exist
        # deduplicated_data = list(seen.values())
        with conn.cursor() as cur:
            query = f"""
            INSERT INTO metro_db_{store_id}(product_id, product_name, package_size, current_price, previous_price) VALUES %s
            ON CONFLICT(product_id)
            DO UPDATE SET
            product_name = EXCLUDED.product_name,
            package_size = EXCLUDED.package_size,
            current_price = EXCLUDED.current_price,
            previous_price = EXCLUDED.previous_price;
            """
            execute_values(cur,query,data)
        conn.commit()    
    except Error as e:
        print(f"Error inserting to table: {e}")


def save_scraped_data(data,store_id):
    conn = connect_to_database()
    if conn:
        try:
            create_table(conn,store_id)
            insert_data(conn,data, store_id)
        finally:
            conn.close()
            
            
"""Functions to store store informations"""

def create_store_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS metro_store_data(
                            store_id        VARCHAR(5) PRIMARY KEY,
                            store_name      VARCHAR(255),
                            store_street    VARCHAR(255),
                            store_city      VARCHAR(255),
                            store_province  VARCHAR(5),
                            store_postal    VARCHAR(10),
                            store_cookie    VARCHAR(255)
                        );
                        """)
            conn.commit()
    except Error as e:
        print(f"Error creating table: {e}")

def insert_store_data(conn,data):
    try:
        with conn.cursor() as cur:
            query = """
            INSERT INTO metro_store_data(store_id,store_name,store_street,store_city,store_province,store_postal,store_cookie) VALUES %s
            ON CONFLICT(store_id)
            DO UPDATE SET
            store_name = EXCLUDED.store_name,
            store_street = EXCLUDED.store_street,
            store_city = EXCLUDED.store_city,
            store_province = EXCLUDED.store_province,
            store_postal = EXCLUDED.store_postal,
            store_cookie = EXCLUDED.store_cookie;
            """
            execute_values(cur, query,data)
        conn.commit()
    except Error as e:
        print(f"Error inserting data: {e}")
        
def save_store_data(data):
    conn = connect_to_database()
    if conn:
        try:
            create_store_table(conn)
            insert_store_data(conn,data)
        finally:
            conn.close()
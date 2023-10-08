import random
import string
import pymysql
import hashlib
import os
import csv
import datetime
import json

"""
Tables list
-- customers*
-- Coupons*
-- Orders *
-- Products*
-- Order_items* 
-- Categories *
-- Product_categories

"""

# TODO: make names more releastic

US_STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
             "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND",
             "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


# List of common domain names for email addresses
common_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'aol.com', 'hotmail.com', 'icloud.com', 'mail.com',
                  'protonmail.com', 'zoho.com', 'yandex.com', 'mail.ru', 'gmx.com', 'tutanota.com', 'fastmail.com',
                  'hushmail.com', 'centurylink.net', 'comcast.net', 'verizon.net', 'att.net', 'cox.net',
                  'sbcglobal.net', 'charter.net', 'roadrunner.com']


# Define the sample categories as a list
categories = ["Clothing", "Shoes", "Accessories", "Electronics", "Home & Garden", "Sports & Outdoors",
              "Beauty & Personal Care", "Toys & Games", "Books & Media", "Food & Beverage"]



class SampleDataGenerator:

    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = pymysql.connect(**db_config)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.script_path = os.path.dirname(__file__)

    # Generate a random string of characters for testing purposes
    def random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    # Generate a random date
    def random_date(self):
        start_date = datetime.date(2010, 1, 1)
        end_date = datetime.date(2022, 1, 1)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        return random_date.strftime("%Y-%m-%d")

    # Method to insert sample data into the Customers table
    def insert_customers(self, qty):
        """Creates random customers records"""

        with open(os.path.join(self.script_path, 'first_names.csv'), 'r') as f:
            first_names_raw = f.readlines()
        random.shuffle(first_names_raw)
        first_names = [i.strip() for i in first_names_raw]

        with open(os.path.join(self.script_path, 'last_names.csv'), 'r') as f:
            last_names_raw = f.readlines()
        random.shuffle(last_names_raw)
        last_names = [i.strip() for i in last_names_raw]

        # Generate a random set of customer data
        customer_data = []
        for _ in range(int(qty)):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name}.{last_name}@{random.choice(common_domains)}"
            password = self.random_string(8)

            salt = os.urandom(16) # Generate a random salt
            hashed_password = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()

            address = f"{random.randint(1, 100)} {self.random_string(10).capitalize()}"
            city = self.random_string(7)
            state = random.choice(US_STATES)
            zip_code = str(random.randint(10000, 99999))
            customer_data.append((first_name, last_name, email, hashed_password, address, city, state, zip_code))

        # Insert the customer data into the database
        query = "INSERT INTO customers (first_name, last_name, email, password, address, city, state, zip_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.executemany(query, customer_data)
        self.conn.commit()
        print(self.cursor.rowcount, "customers inserted.")

    def get_all_existing_customers(self):
        self.cursor.execute("SELECT customer_id FROM customers")
        customers = [row for row in self.cursor.fetchall()]
        return customers

    # Method to insert sample coupons
    def insert_coupons(self, num_coupons):
        """Generate sample coupon data and insert into the 'coupons' table."""

        chars = string.ascii_uppercase + string.digits
        coupons = []
        for i in range(num_coupons):
            coupon_code = ''.join(random.choices(chars, k=10))
            discount_percentage = random.choice([20, 25, 50, 60, 75, 100])
            expiration_date = datetime.date.today() + datetime.timedelta(days=random.randint(30, 365))
            coupon = (coupon_code, discount_percentage, expiration_date)
            coupons.append(coupon)

        insert_query = "INSERT INTO coupons (coupon_code, discount_percentage, expiration_date) VALUES (%s, %s, %s)"
        self.cursor.executemany(insert_query, coupons)
        self.conn.commit()
        print(f"{num_coupons} coupons generated and inserted successfully!")

    def get_all_existing_coupons(self):
        self.cursor.execute("SELECT coupon_id, discount_percentage FROM coupons")
        coupons = [row for row in self.cursor.fetchall()]
        return coupons

    def insert_products_from_csv(self):
        csv_path = os.path.join(self.script_path, 'product_name_list.csv')
        product_list = []
        with open(csv_path, 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data) # to skip header row
            for row in csv_data:
                product_name = row[0]
                description = self.random_string(random.randint(100, 200))
                price = round(random.uniform(10, 100), 2)
                image_url = "https://demostore.supersqa.com/" + self.random_string(random.randint(10, 30))
                product_list.append((product_name, description, price, image_url))

        # Insert the customer data into the database
        query = "INSERT INTO products (product_name, description, price, image_url) VALUES (%s, %s, %s, %s)"
        self.cursor.executemany(query, product_list)
        self.conn.commit()
        print(self.cursor.rowcount, "products inserted.")

    def insert_products_from_json_file(self):

        json_path = os.path.join(self.script_path, 'products_list.json')
        with open(json_path, 'r') as f:
            all_products = json.load(f)

        product_list = []
        for product in all_products:
            product_list.append((product['product_name'], product['description'], product['price'], product['image_url']))

        # Insert the customer data into the database
        query = "INSERT INTO products (product_name, description, price, image_url) VALUES (%s, %s, %s, %s)"
        self.cursor.executemany(query, product_list)
        self.conn.commit()
        print(self.cursor.rowcount, "products inserted.")

    def insert_categories(self):
        query = "INSERT INTO Categories (category_name) VALUES (%s)"
        categories_to_insert = [(i) for i in categories]
        self.cursor.executemany(query, categories_to_insert)
        self.conn.commit()
        print(self.cursor.rowcount, "categories inserted.")

    def get_all_existing_categories(self):
        self.cursor.execute("SELECT category_id FROM Categories")
        categories = [row for row in self.cursor.fetchall()]
        return categories

    def insert_product_categories(self):
        all_products = self.get_all_existing_products()
        all_categories = self.get_all_existing_categories()
        all_category_ids = [i['category_id'] for i in all_categories]

        all_product_categories = []
        for product in all_products:
            all_product_categories.append((product['product_id'], random.choice(all_category_ids)))
        query = "INSERT INTO product_categories (`product_id`, `category_id`) VALUES (%s, %s);"
        self.cursor.executemany(query, all_product_categories)
        self.conn.commit()
        print(self.cursor.rowcount, "product categories inserted.")


    def get_all_existing_products(self):
        self.cursor.execute("SELECT product_id, price FROM products")
        products = [row for row in self.cursor.fetchall()]
        return products

    def create_order_record(self, cust_id, order_date, total_price):

        sql = f"INSERT INTO Orders (customer_id, order_date, total_price) VALUES ({cust_id}, '{order_date}', {total_price})"
        self.cursor.execute(sql)
        self.conn.commit()
        order_id = self.cursor.lastrowid

        return order_id

    def create_data_for_order_and_order_line(self, number_of_orders):
        """

        example_order = {
            'order_id': 11,
             'customer_id': 12,
             'order_date': 154,
             'total_price': 'tbd',
             'line_items':
                     [
                         {
                             'item_id': 11,
                             'order_id': 11,
                             'product_id': 11,
                             'quantity': 11,
                             'price': 11,
                             'coupon_id': 11
                         }
                     ]
                 }
        :param number_of_orders:
        :return:
        """

        all_available_products = self.get_all_existing_products()
        all_available_coupons = self.get_all_existing_coupons()
        all_available_customers = self.get_all_existing_customers()

        all_orders = []
        for _ in range(int(number_of_orders)):
            order = {}
            order['total_price'] = 'tbd'
            order['customer_id'] = random.choice(all_available_customers)['customer_id']
            order['order_date'] = '2023-03-05'

            # some orders will have multiple order lines and some will have only 1. More orders should have 1 item only.
            item_qty = random.choice([1, 1, 1, 2, 2, 3, 4, 5])
            total_price_for_order = 0
            order_items = []
            for i in range(item_qty):
                order_item = {}
                product = random.choice(all_available_products)
                order_item['product'] = product
                order_item['quantity'] = random.randint(1, 6)
                order_item['original_item_price'] = product['price']
                coupon = random.choice(all_available_coupons)
                order_item['coupon'] = coupon

                # calculate to total paid for particular item. Considering multiple instance of one object
                discount_pct = coupon['discount_percentage']
                paid_price_each = float(product['price']) - (float(product['price']) * float(discount_pct)/100)
                price_paid_total_item = order_item['quantity'] * paid_price_each
                order_item['final_price'] = price_paid_total_item

                # calculate total for all items in the order
                total_price_for_order += price_paid_total_item

                # collect items in the order
                order_items.append(order_item)

            order['line_items'] = order_items
            order['total_price'] = total_price_for_order

            all_orders.append(order)

        return all_orders

    def create_orders_and_line_db_records(self, number_of_orders):
        print(f"Number of orders to be created: {number_of_orders}")
        orders_data = self.create_data_for_order_and_order_line(number_of_orders)
        order_item_sql = """INSERT INTO order_items ( `order_id`, `product_id`, `quantity`, `price`, `coupon_id`, `original_item_price`) 
                            VALUES ({order_id}, {product_id}, {quantity}, {price}, {coupon_id}, {original_item_price});"""
        total_line_item_count = 0
        for order in orders_data:
            order_id = self.create_order_record(order['customer_id'], order['order_date'], order['total_price'])
            line_items = order['line_items']
            total_line_item_count += len(line_items)
            for item in line_items:
                self.cursor.execute(
                    order_item_sql.format(
                                    order_id=order_id,
                                    product_id=item['product']['product_id'],
                                    quantity=item['quantity'],
                                    price=item['final_price'],
                                    original_item_price=item['original_item_price'],
                                    coupon_id=item['coupon']['coupon_id']
                                        )
                                    )
                self.conn.commit()

        print(f"Number of orders created: {number_of_orders}")
        print(f"Number of order items created: {total_line_item_count}")


if __name__ == '__main__':

    # User Settings
    db_config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': 8889,
        'database': 'ecomm_store'
    }

    number_of_customers = 200
    number_of_orders = 500
    number_of_coupons = 25

    # Start generating data
    data_generator = SampleDataGenerator(db_config)

    data_generator.insert_customers(number_of_customers)
    # data_generator.insert_products_from_csv()
    data_generator.insert_products_from_json_file()
    data_generator.insert_coupons(number_of_coupons)
    data_generator.create_orders_and_line_db_records(number_of_orders)
    data_generator.insert_categories()
    try:
        data_generator.insert_product_categories()
    except Exception as e:
        if "Duplicate" in str(e):
            pass
        else:
            raise


CREATE DATABASE IF NOT EXISTS foobar;

USE foobar;

SOURCE ./create_table_products.sql;
SOURCE ./create_table_orders.sql;
-- SOURCE /Users/akinfu/chegg/misc/sql-course/sample_data/example-database-ecommerce/try_option_2/create_table_products.sql;


-- 12:37:40	source ./create_table_products.sql	Error Code: 1064. You have an error in your SQL syntax; c
-- heck the manual that corresponds to your MySQL server version for the right syntax to use near 'source ./create_table_products.sql' at line 1	0.00029 sec
-- Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL 
-- server version for the right syntax to use near 'source /Users/akinfu/chegg/misc/sql-course/sample_data/example-database-ecommerc' at line 1

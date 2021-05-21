#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 17:39:14 2021

@author: john
"""
# DROP TABLES
crm_table_drop = "DROP TABLE IF EXISTS crm"
sales_table_drop = "DROP TABLE IF EXISTS sales"


# CREATE TABLES
crm_table_create = (""" CREATE TABLE IF NOT EXISTS crm (crm_id SERIAL, account_id varchar(250), \
                         event_type varchar(200) NOT NULL, event_date date NOT NULL,
                         PRIMARY KEY(crm_id))
""")


sale_table_create = (""" CREATE TABLE IF NOT EXISTS sales (sale_id SERIAL, account_id varchar(250),
                            product_name varchar(100) NOT NULL, date date NOT NULL,
                            unit_sales int NOT NULL, created_time timestamp NOT NULL,
                            PRIMARY KEY(sale_id))
""")


# INSERT RECORDS
crm_table_insert = (""" INSERT INTO crm (account_id, event_type, \
                         event_date) VALUES(%s, %s, %s) \
                                ON CONFLICT (crm_id) \
                                    DO NOTHING;
""")

sales_table_insert = (""" INSERT INTO sales (account_id, product_name, date, unit_sales,
                      created_time) VALUES(%s, %s, %s, %s, %s) \
                                ON CONFLICT (sale_id) \
                                    DO NOTHING;
""")

# QUERY LISTS
create_table_queries = [crm_table_create, sale_table_create]

drop_table_queries = [crm_table_drop, sales_table_drop]

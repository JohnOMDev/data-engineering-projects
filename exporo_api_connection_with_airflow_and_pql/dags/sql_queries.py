#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 06:48:37 2021

@author: john
"""

investment_table_drop = "DROP TABLE IF EXISTS investments"
available_volume_table_drop = "DROP TABLE IF EXISTS available_volumes"
funding_target_table_drop = "DROP TABLE IF EXISTS funding_targetS"
intermediated_capital_table_drop = "DROP TABLE IF EXISTS intermediated_capitalS"

investment_table_create = ("""
  CREATE TABLE IF NOT EXISTS investments
  (
   "Investment Id" SERIAL,
    "Financing Entity ID" INTEGER,
    "Date" DATE,
    "Contract ID" INTEGER,
    Name VARCHAR(250),
    Image VARCHAR(1000),
    "Investment Rate"  DECIMAL(5,2),
    "Investment Type" VARCHAR(100),
    "Minimum Investment" DECIMAL(10,2),
    "Duration Investor Min" DATE,
    "Duration Investor Max" DATE,
    "Maximum Investment" DECIMAL(10,2),
    PRIMARY KEY("Investment Id")
    )
""")

available_volume_table_create = ("""
    CREATE TABLE IF NOT EXISTS available_volumes
      (
        "Financing Entity ID" INTEGER,
        "Available Volume" DECIMAL(20,2),
        "Date" DATE
        )
""")

investment_table_insert = (""" INSERT INTO investments("Financing Entity ID",
                                                    "Date",
                                                    "Contract ID",
                                                    Name,
                                                    Image,
                                                    "Investment Rate",
                                                    "Investment Type",
                                                    "Minimum Investment",
                                                    "Duration Investor Min",
                                                    "Duration Investor Max",
                                                    "Maximum Investment") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

available_volume_table_insert = ("""
    INSERT INTO available_volumes("Financing Entity ID", "Available Volume", "Date")
    SELECT DISTINCT 
                ft."Financing Entity ID",
                (ft."Funding Target" - 
                ic."Intermediated Capital") as "Available Volume",
                ic."Date"
    FROM  funding_target as ft
    INNER JOIN  intermediated_capital as ic ON ft."Financing Entity ID" = ic."Financing Entity ID"
""")

funding_target_table_create = ("""
    CREATE TABLE funding_target
        ("Financing Entity ID" int, "Funding Target" int)
        
    INSERT INTO funding_target
        ("Financing Entity ID", "Funding Target")
    VALUES
        (212, 2500000.00),
        (3168, 2000000.00),
        (5826, 2400000.00),
        (981, 2600000.00)

""")

funding_target_table_create = ("""
    CREATE TABLE  intermediated_capital
        ("Financing Entity ID" int, "Date" timestamp, "Intermediated Capital" int)
    
    INSERT INTO  intermediated_capital
        ("Financing Entity ID", "Date", "Intermediated Capital")
    VALUES
        (212, '2019-02-01 00:00:00', 2000000.00),
        (212, '2019-02-02 00:00:00', 300000.00),
        (212, '2019-02-03 00:00:00', 200000.00),
        (3168, '2020-01-15 00:00:00', 1000000.00),
        (3168, '2020-01-16 00:00:00', 500000.00),
        (3168, '2020-01-17 00:00:00', 300000.00),
        (3168, '2020-01-18 00:00:00', 200000.00)

""")

# QUERY LISTS
insert_table_queries = [available_volume_table_insert]
create_table_queries = [investment_table_create, available_volume_table_create, funding_target_table_create,
                        funding_target_table_create]
drop_table_queries = [investment_table_drop, available_volume_table_drop, funding_target_table_drop,
                      intermediated_capital_table_drop]

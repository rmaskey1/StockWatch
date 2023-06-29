from scraper import get_stock_list, real_time_price
import psycopg2
import re
import timeit

conn = psycopg2.connect(
    host="localhost",
    database="StockWatch",
    user="postgres",
    password="admin"
)

def convert_percentage_to_float(percentage):
    if percentage.endswith("%"):
        percentage = percentage[:-1]  # Remove the percent sign at the end
    if percentage.startswith("-"):
        percentage = percentage[1:]  # Remove the leading minus sign for negative percentages
        multiplier = -1.0
    else:
        multiplier = 1.0

    result = float(percentage)  # Convert the remaining string to a float and divide by 100
    result *= multiplier  # Apply the multiplier to handle negative percentages
    return result

def populate_stock_data():
    stocks = get_stock_list()
    cursor = conn.cursor()
    cursor.execute('TRUNCATE TABLE stock RESTART IDENTITY CASCADE')
    for symbol, name in stocks.items():
        start = timeit.default_timer()
        last_price, price_change, percent_change = real_time_price(symbol)
        end = timeit.default_timer()
        print("Time taken for real time price:", end-start)

        start = timeit.default_timer()
        if "," in last_price:
            last_price = last_price.replace(",","")
        if "," in price_change:
            price_change = price_change.replace(",","")
        percent_change = percent_change[1:-1]
        percent_change = convert_percentage_to_float(percent_change)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO stock (stock_code, stock_name, last_price, price_change, percent_change) VALUES (%s,%s,%s,%s,%s)', (symbol, name, last_price, price_change, percent_change,))
        conn.commit()
        print("inserted")
        end = timeit.default_timer()
        print("Time taken for data clean up and insertion", end-start)
    cursor.close()

populate_stock_data()
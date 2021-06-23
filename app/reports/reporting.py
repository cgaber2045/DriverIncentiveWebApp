from ..database.db_users import getConnection
from io import StringIO, BytesIO
from datetime import datetime
from functools import reduce
import csv
import calendar

class ReportController():
    def __init__(self):
        self.conn = getConnection()
        self.file = CSVManager()
    
    def number_users(self, userType):
        sql = "SELECT COUNT(*) FROM {}".format(userType)
        
        try:
            num = self.conn.exec(sql)
            return num[0][0] if num else 0
        except Exception as e:
            return 0

    def sponsor_stats(self, sid, dates=()):
        """ Get statistics about each sponsor in a date range 
            dates: tuple(start_date, end_date)
        """
        sql = "SELECT Order_ID, TimeStamp, amount FROM Product_Orders WHERE Sponsor_Id=%s AND TimeStamp BETWEEN %s AND %s"
        start = dates[0].month
        end = dates[1].month
        vals = (sid, dates[0], dates[1])

        try:
            orders = self.conn.exec(sql, vals)

            # This long line creates a dictionary of every month for a given sponsor and sums all the purchases for that month
            # Kind of a long convoluted way to do it, but it's fun to try and do things with lambdas and functional methods
            results = dict(map(lambda i: (i, reduce(lambda x,y: x + y, map(lambda o: o[-1], filter(lambda order: order[1].month == i, orders)), 0)), range(start,end+1)))
            return results

        except Exception as e:
            print(e)
            return None

    def total_sales(self, dates=()):
        """ Get total amount of sales per month in date range """
        sql = "SELECT Order_ID, TimeStamp, amount FROM Product_Orders WHERE TimeStamp BETWEEN %s AND %s"
        
        try:
            orders = self.conn.exec(sql, dates)
            months = dict(map(lambda i: (i, reduce(lambda x,y: x + y, map(lambda o: o[-1], filter(lambda order: order[1].month == i, orders)), 0)), range(dates[0].month,dates[1].month+1)))

            return months
        except Exception as e:
            print(e)
            return None

    def driver_purchases(self, sid): 
        """ Get list of all drivers and their purchases that are affilated with sponsor sid """
        sql = "SELECT user, name, amount FROM Product_Orders NATURAL JOIN driver, product WHERE Product_Orders.Product_ID=product.product_id AND Product_Orders.Sponsor_ID=%s"

        try:
            orders = self.conn.exec(sql, (sid, ))
            names = list(map(lambda e: e[0], orders))

            drivers = dict(map(lambda e: (e, []), names))

            def func(order):
                drivers[order[0]].append(order[1])
                return order

            orders = tuple(map(func, orders))
            return drivers
        except Exception as e:
            print(e)
            return None

    def write(self, row: tuple):
        self.file.writerow(row)

    def get_file(self):
        return self.file.create()
    def __del__(self):
        self.conn.close()

class CSVManager():
    def __init__(self):
        self.stream = StringIO()
        self.writer = csv.writer(self.stream)

    def writerow(self, row: tuple):
        self.writer.writerow(row)

    def create(self):
        mem = BytesIO()
        mem.write(self.stream.getvalue().encode('utf-8'))
        mem.seek(0)
        self.stream.close()
        return mem

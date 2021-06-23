import json
import os
from ..database.db_users import getConnection
from .etsy_driver import EtsyController

class CatalogController():
    """ Definition of a catalog item found in api_routes"""
    def __init__(self):
        self.conn = getConnection()

    def insert(self, item: dict, sponsor_id):
        """ item is dict from JSON submitted through API 
            and returns whether or not the items was added to the database """
        sql = """ INSERT INTO product (name, description, price, img_url, listing_id, sponsor_id) VALUES
                  (%(title)s, %(description)s, %(price)s, %(img_url)s, %(listing_id)s, {}) """.format(sponsor_id)
        
        # Raise exception if item in database already
        if self.item_in_db(item['listing_id'], sponsor_id):
            raise ItemInDB("Item already in database")

        try:
            self.conn.exec(sql, item)
            return True
        except Exception as e:
            return False

    def fetch_catalog_items(self, sponsor_id, search = None):
        sql = "SELECT name, description, price, listing_id, img_url FROM product WHERE sponsor_id=%s"
        if search:
            sql += " AND (name REGEXP '{}' OR description REGEXP '{}')".format(search, search)

        try:
            out = self.conn.exec(sql, (sponsor_id, ))
            items = list(map(lambda elem:
                                   {
                                        'title': elem[0],
                                        'description': elem[1],
                                        'price': elem[2],
                                        'listing_id': elem[3],
                                        'img_url': elem[4]
                                    },
                             out
                             )
                        )
            return {'items': items}
        except Exception as e:
            print(e)
            return {'items': []}

    def fetch_all_items(self):
        sql = "SELECT product_id FROM product"

        try:
            out = self.conn.exec(sql)
            items = [x[0] for x in out]
            return {'items': items}

        except Exception as e:
            print(e)
            return {'items': []}


    def remove(self, sponsor_id, item_id):
        sql = "DELETE FROM product WHERE sponsor_id=%s and listing_id=%s"
        vals = (sponsor_id, item_id)
        
        try:
            self.conn.exec(sql, vals)
            return True
        except Exception as e:
            print(e)
            return False

    def item_in_db(self, listing_id, sponsor_id):
        """ item_in_db = True iff listing_id and sponsor_id pair is contained in database"""
        sql = "SELECT COUNT(*) FROM product WHERE listing_id=%s AND sponsor_id=%s"
        
        try:
            # Will be 0
            out = self.conn.exec(sql, (listing_id, sponsor_id))
            if out:
                return out[0][0] > 0
            print(num)
        except Exception as e:
            return False
    
    def unlist_product(self, product_id):
        """ Change the available flag of a product to False """
        sql = "UPDATE product SET available=0 WHERE product_id=%s"

        try:
            out = self.conn.exec(sql, (product_id, ))
            return True
        except Exception as e:
            print(e)
            return False

    def update_price(self, product_id):
        """ Update the price of a product in the database from Etsy """
        cont = EtsyController(os.getenv('ETSY_API_KEY'))

        # Find item in database and get its listing id
        listing_id = 0
        try:
            q = "SELECT listing_id FROM product WHERE product_id=%s"
            results = self.conn.exec(q, (product_id, ))
            if results:
                listing_id = results[0][0]
            else:
                del cont
                return None
        except Exception as e:
            print(e)
            del cont
            return None

        sql = "UPDATE product SET price = %s WHERE product_id=%s"

        item = cont.get_current_price(listing_id)

        # Check if item is no longer available
        if not item:
            self.unlist_product(product_id)
            return None

        vals = (item['price'], product_id)

        # If it runs without error, it is assumed that the price is updated
        try:
            self.conn.exec(sql, vals)
            sql = "SELECT * FROM product WHERE product_id=%s"
            out = self.conn.exec(sql, (product_id, ))

            del cont
            return out[0] if out else None


        except Exception as e:
            print(e)
            del cont
            return None

    def __del__(self):
        global pool1
        self.conn.close()

class ItemInDB(Exception):
    pass

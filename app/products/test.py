from etsy_driver import EtsyController

api_key='5gzqdrc6x4n1sfgqfqa1b7tq'
conn = EtsyController(api_key)
conn.limit = 1

items = conn.get_products_keywords('mittens')
print(type(items))
for item in items:
    print(item)

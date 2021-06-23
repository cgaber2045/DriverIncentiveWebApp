from etsy2 import Etsy
import json

class EtsyController():
    """ Controller class for talking to the Etsy API. Will return useful results based off of need """

    def __init__(self, api_key=''):
        self.conn = Etsy(api_key=api_key)
        self.limit = 25

    def get_products_keywords(self, keywords=''):
        # Get product name, description, tags, and URL
        results = self.conn.findAllListingActive(keywords=keywords, limit=self.limit, includes="Images")

        #print(results[0].keys())
        needed_elems = ['title', 'description', 'price', 'url', 'views', 'listing_id', 'Images']
        for i in range(0,len(results)):
            results[i] = dict(filter(lambda elem: elem[0] in needed_elems, results[i].items()))
            try:
                results[i]['Images'] = results[i]['Images'][0]['url_170x135']
            except IndexError as e:
                print(results[i]['Images'])
        return results

    def get_products_tags(self, tags=[]):
        
        results = self.conn.findAllListingActive(tags=tags, limit=self.limit)
        needed_elems = ['title', 'description', 'price', 'url']

        for i in range(0, len(results)):
            results[i] = dict(filter(lambda elem: elem[0] in needed_elems, results[i]))
        return results

    def get_products_images(self, pids=[]):
        results = []
        results = list(map(lambda pid: self.conn.getImage_Listing(listing_id=pid), pids))
        return results

    def get_product_id(self, pid=''):
        results = self.conn.getListing(listing_id=pid)
        results = json.loads(results)
        return results

    def get_url(self, pid=''):
        result = self.conn.getListing(listing_id=pid)
        return result[0]['url'] if result and result[0]['state'] == 'active' else ''

    def get_current_price(self, pid):
        """ Grab current price of an item from Etsy by using its listing id """
        needed_elems = ['title', 'price', 'url', 'listing_id']
        results = self.conn.getListing(listing_id=pid)

        if results[0]['state'] != 'active':
            return None
        else:
            return {'price': results[0]['price']}

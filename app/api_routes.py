from flask_restx import Resource, fields
from flask_restx import reqparse
from flask import request
from werkzeug.security import check_password_hash
from app import api, app, admin_api
from app.products.catalog import CatalogController, ItemInDB
from app.database.db_users import *
from app.database.db_functions import get_table_id, get_password
from itsdangerous import (TimedJSONWebSignatureSerializer
                            as Serializer, BadSignature, SignatureExpired)
from functools import wraps
import os

# Generate timed and encrypted JSON token
def generate_auth_token(sponsor_username, expiration = 3600):
    s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
    db = getConnection()
    query = "SELECT sponsor.sponsor_id FROM sponsor JOIN sponsor_logins ON sponsor.sponsor_id=sponsor_logins.sponsor_id WHERE username=%s"
    results = db.exec(query, (sponsor_username, ))
    db.close()
    del db
    if results:
        return s.dumps({'id': results[0][0]})
    else:
        return None

def generate_admin_token(aid, expiration=3600):
    s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
    return s.dumps({'id': aid})
# Check if token is valid
def verify_auth_token(token):
    # Fetch token from database
    s = Serializer(app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except SignatureExpired:
        return False
    except BadSignature:
        return False
    return True

def get_id(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        return data['id']
    except SignatureExpired:
        return None
    except BadSignature:
        return None


# Decorator to do token based auth
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
            if not token:
                return {'message': 'Token is missing'}, 401

            if not verify_auth_token(token):
                return {'message': 'Your token is bad. Generate a new one.'}, 401
            print('TOKEN: {}'.format(token))
            return f(*args, **kwargs)
        else:
            return {'message': 'Token is missing'}, 401
    return decorated

# Catalog JSON description
catalog_item = api.model('Catalog_Item', {
    'title': fields.String,
    'price': fields.Float,
    'description': fields.String,
    'img_url': fields.Url,
    'listing_id': fields.Integer
})

# Full catalog view
catalog = api.model('Catalog', {
    'items': fields.List(fields.Nested(catalog_item))
})

@api.route('/catalog')
@api.doc(security='apikey')
class SponsorCatalog(Resource):

    @token_required
    @api.marshal_with(catalog)
    def get(self):
        id = get_id(request.headers['X-API-KEY'])
        cont = CatalogController()
        out = cont.fetch_catalog_items(id)
        print(out)
        del cont
        return out

    @token_required
    @api.expect(catalog_item)
    def post(self):
        id = get_id(request.headers['X-API-KEY'])
        item = api.payload
        cont = CatalogController()
        try:
            added = cont.insert(item, id)
            del cont

            if added:
                return {'message': 'Item added'}, 200
            else:
                return {'message': 'Item not added'}, 400

        except ItemInDB:
            return {'message': 'Item already in database'}, 400
            
        del cont
        if added:
            return {'message': 'Item added'}, 200
        else:
            return {'message': 'Item not added'}, 400
        
    @token_required
    @api.expect(api.model('Listing', {'listing_id': fields.Integer}))
    def delete(self):
        id = get_id(request.headers['X-API-KEY'])
        listing = api.payload['listing_id']
        cont = CatalogController()
        val = cont.remove(id, listing)
        del cont
        if val:
            return {'message': 'Item removed'}
        else:
            return {'message': 'Item not removed'}

@api.route('/auth/<string:sponsor_username>')
class SponsorAPIAuth(Resource):
    def get(self, sponsor_username):
        token = generate_auth_token(sponsor_username)
        if token:
            return {'token': token.decode('ascii')}, 200
        else:
            return {'message': 'Sponsor name not found'}, 400

product = admin_api.model('Product', {
    'id': fields.Integer
})

product_list = admin_api.model('Product_List', {
    'ids': fields.List(fields.Integer)
})

@admin_api.route('/products')
@admin_api.doc(security='apikey')
class AdminProductAPI(Resource):

    @token_required
    def get(self):
        cont = CatalogController()
        items = cont.fetch_all_items()
        return items

    @admin_api.expect(product_list)
    @token_required
    def put(self):
        data = api.payload
        cont = CatalogController()

        _ = list(map(lambda id: cont.update_price(id), data['ids']))
        del cont
        return {'message': 'success'}

@admin_api.route('/auth')
class AdminAPIAuth(Resource):
    @admin_api.expect(admin_api.model('Credentials', {'username': fields.String, 'password': fields.String}))
    def post(self):
        data = api.payload
        print(data)
        try:
            uid, role = get_table_id(data['username'])
        except Exception as e:
            print(e)
            return {'message': 'Unauthorized'}, 401

        if role != 'admin':
            return {'message': 'Unauthorized'}, 401

        curHash = get_password(data['username'])

        if check_password_hash(curHash, data['password']):
            token = generate_admin_token(uid)
            return {'message': 'success', 'content': {'username': data['username'], 'token': token.decode('ascii')}}
        else:
            return {'message': 'Incorrect credentials'}, 200

    @admin_api.doc(security='apikey')
    @token_required
    def get(self):
        return 'You passed!'
        pass

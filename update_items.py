import requests as r

# These need to be changed to an active admin account in the system, along with the actual URI of the project
USER = 'changeme'
PWD = 'example!'
URL = 'http://localhost:5000/admin/api'
def main():
    # Get API token
    conn = r.post(URL + '/auth', json={'username': USER, 'password': PWD})
    token = None

    # Try to get message and set token
    try:
        data = conn.json()
        if data['message'] == 'success':
            token = data['content']['token']
        else:
            print(data['message'])
            quit()

    except Exception as e:
        print(e)
        print('Weird result')
        quit()
    
    # Add token to headers
    headers = {'X-API-KEY': token}
    conn = r.get(URL + '/products', headers=headers)

    # Get list of products and update prices
    try:
        data = conn.json()
        ids = data['items']

        try:
            conn = r.put(URL + '/products', headers=headers, json={'ids': ids})
        except Exception as e:
            print('Another weird error')
            quit()

    except Exception as e:
        print('This should not happen')
        quit()

    print('All done')

if __name__ == '__main__':
    main()

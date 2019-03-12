import sys

from requests.auth import HTTPBasicAuth
import requests
import json

# Base da url da API
BASE_URL = 'https://api.github.com'
# /users/ é o endpoint para buscar usuários do Github
SEARCH_ONE_URL = BASE_URL + '/users/'
# Entra autenticado na API
AUTH_URL = BASE_URL + '/authorizations'
# Busca usuários
SEARCH_URL = BASE_URL + '/search/users'

GENERIC_HEADER = {"User-Agent": 'Find Some Candidates'}
PREVIEW_HEADER = {"Accept": 'application/vnd.github.preview'}
PREVIEW_HEADER.update(GENERIC_HEADER)
# Query de busca
SEARCH_QUERY = 'location:Teresina'

# Autenticação para fazer as buscas
CREDS = ('q721384', 'rB^(0<:8eebQ#,m')


def get_access_token(username, password):
    auth_payload = {
        'client_id': '111de754c948895a4601',
        'client_secret': '30506b2f0a71e33be99e57ecdb71670554e7aa8f',
        'scopes': 'user'
    }

    auth_res = requests.post(
        AUTH_URL, data=json.dumps(auth_payload),
        auth=HTTPBasicAuth(username, password),
        headers=GENERIC_HEADER)

    if auth_res.status_code in [200, 201]:
        return auth_res.json()['token']
    return None


def search_for_users(query, token):
    payload = {
        'q': query,
        'access_token': token,
        'sort': 'followers',
        'per_page': 100,
    }

    first_res = requests.get(SEARCH_URL, params=payload,
                             headers=PREVIEW_HEADER)

    results = first_res.json()
    users = results.get('items', [])
    total_count = results.get('total_count', 0)

    url = [u["url"] for u in users]
    for i in url:
        search_hireable_by_user = requests.get(i + "?client_id=111de754c948895a4601&client_secret=30506b2f0a71e33be99e57ecdb71670554e7aa8f")
        print(search_hireable_by_user.json())
        # Pegar os json -> hireable


    if total_count > 100:
        pages = results['total_count'] // 100
        for i in range(2, int(pages + 2)):
            payload['page'] = i
            res = requests.get(SEARCH_URL, params=payload,
                               headers=PREVIEW_HEADER)
            results = res.json()
            users.extend(results.get('items', []))
    return users


def get_user_details(user, token):
    payload = {
        'access_token': token,
    }
    res = requests.get(SEARCH_ONE_URL + user['login'], params=payload)

    if res.status_code == 200:
        user['details'] = res.json()


if __name__ == '__main__':
    if 'CREDS' not in globals():
        if len(sys.argv) > 1:
            if len(sys.argv) == 2:
                # use token for authentication
                access_token = sys.argv[1]
            if len(sys.argv) > 2:
                access_token = get_access_token(*sys.argv[1:3])
        else:
            sys.exit(__doc__)
    else:
        # A definir o que acontece
        access_token = get_access_token(*globals()['CREDS'])

    users = search_for_users(SEARCH_QUERY, access_token)
    for user in users:
        get_user_details(user, access_token)
    # f = open('candidates_dump.json', 'w')
    # f.write(json.dumps(users))
    # f.close()

    # hirable = [u['login'] for u in users if u.get('details', {}).get('hireable', False)]
    # f = open('vertices.json', 'w')
    # f.write(json.dumps(hirable))
    # f.close()

    print("Ainda não há algo certo para o else")

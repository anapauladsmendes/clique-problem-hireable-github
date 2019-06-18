import sys
import requests
import ujson as json
from requests.auth import HTTPBasicAuth

BASE_URL = 'https://api.github.com'
USERS_URL = BASE_URL + '/users/'
AUTH_URL = BASE_URL + '/authorizations'
SEARCH_URL = BASE_URL + '/search/users'

GENERIC_HEADER = {"User-Agent": 'Find Some Candidates'}
PREVIEW_HEADER = {"Accept": 'application/vnd.github.preview'}
PREVIEW_HEADER.update(GENERIC_HEADER)

SEARCH_QUERY = 'location:Teresina'

USER_GITHUB = ''
PASSWORD = ''
CREDS = (USER_GITHUB, PASSWORD)
CLIENT_ID = ''
CLIENT_SECRET = ''
OAUTH = '?client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET

def get_access_token(username, password):
    auth_payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
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

    ## Users hireable ---------------------------------------------------------------------------------------------------

    j = 0
    list_hireables = []
    user = [u for u in users]
    for i in user:
        search_hireable_by_user = requests.get(i['url'] + OAUTH)
        object_user = search_hireable_by_user.json()
        hireable = object_user['hireable']
        if hireable == True:
            list_hireables.append(i['login'])
            print(i['login'] + " - hireable: " + str(hireable))
            j += 1

    f = open('users_hireable_brute_force.json', 'w')
    f.write(json.dumps(list_hireables))
    f.close()

    ## -----------------------------------------------------------------------------------------------------------------

    ## Find cliques ----------------------------------------------------------------------------------------------------

    list_of_reciprocity = []

    for i in range(0, j):
        for l in range(i + 1, j):
            check_follow = requests.get(USERS_URL + list_hireables[i] + "/following/" + list_hireables[l] + OAUTH)
            check_follow_back = requests.get(USERS_URL + list_hireables[l] + "/following/" + list_hireables[i] + OAUTH)
            check_follow = check_follow.status_code
            check_follow_back = check_follow_back.status_code
            print(list_hireables[i] + " following " + list_hireables[l] + "-" + str(check_follow))
            print(list_hireables[l] + " following " + list_hireables[i] + "-" + str(check_follow_back))
            if check_follow == 204 and check_follow_back == 204:
                users = [list_hireables[i], list_hireables[l]]
                list_of_reciprocity.append(users)

    f = open('cliques_brute_force.json', 'w')
    f.write(json.dumps(list_of_reciprocity))
    f.close()
    print(list_of_reciprocity)

    ## -----------------------------------------------------------------------------------------------------------------

    if total_count > 100:
        pages = results['total_count'] // 100
        for i in range(2, int(pages + 2)):
            payload['page'] = i
            res = requests.get(SEARCH_URL, params=payload,
                               headers=PREVIEW_HEADER)
            results = res.json()
            users.extend(results.get('items', []))
    return users

if __name__ == '__main__':
    if 'CREDS' not in globals():
        if len(sys.argv) > 1:
            if len(sys.argv) == 2:
                access_token = sys.argv[1]
            if len(sys.argv) > 2:
                access_token = get_access_token(*sys.argv[1:3])
        else:
            sys.exit(__doc__)
    else:
        access_token = get_access_token(*globals()['CREDS'])

    users = search_for_users(SEARCH_QUERY, access_token)
    print("Encerrou a aplicação!")

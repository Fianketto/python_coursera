import requests


CURRENT_YEAR = 2021
ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
URL_BASE = 'https://api.vk.com/method/'

URL_GET_USER = f'{URL_BASE}users.get?v=5.71&access_token={ACCESS_TOKEN}&user_ids='
URL_GET_FRIENDS_P1 = f'{URL_BASE}friends.get?v=5.71&access_token={ACCESS_TOKEN}&user_id='
URL_GET_FRIENDS_P2 = f'&fields=bdate'


def calc_age(uid):
    get_id_url = f'{URL_GET_USER}{uid}'
    r1 = requests.get(get_id_url).json()
    user_id = r1['response'][0]['id']
    get_friends_url = URL_GET_FRIENDS_P1 + str(user_id) + URL_GET_FRIENDS_P2
    r2 = requests.get(get_friends_url).json()
    friends_dict = {}
    friends_list = []
    for friend in r2['response']['items']:
        try:
            birth_year = friend['bdate'].split('.')[2]
            age = CURRENT_YEAR - int(birth_year)
            friends_dict[age] = friends_dict.get(age, 0) + 1
        except Exception:
            pass
    for k, v in friends_dict.items():
        friends_list.append((k, v))
    friends_list.sort(key=lambda x: x[0])
    friends_list.sort(key=lambda x: x[1], reverse=True)
    return friends_list


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)

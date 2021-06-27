import requests
from requests.auth import HTTPBasicAuth
import json

url = 'https://datasend.webpython.graders.eldf.ru/submissions/1/'


login = "alladin"
password = "opensesame"


resp = requests.post(url=url, auth=HTTPBasicAuth(login, password))
print(resp.text)
for k, v in json.loads(resp.text).items():
    print(k, v)


url2 = 'https://datasend.webpython.graders.eldf.ru/submissions/secretlocation/'
login2 = "alibaba"
password2 = "40razboinikov"

resp = requests.put(url=url2, auth=HTTPBasicAuth(login2, password2))
print(resp.text)
for k, v in json.loads(resp.text).items():
    print(k, v)

'''
echo -n "w3lc0m370ch4p73r4.2" > answer.txt
'''
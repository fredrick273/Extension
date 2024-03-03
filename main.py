import requests
import time

result = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1').json()[0]

user,domain = result.split('@')

print(result)

while True:
    mails = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}").json()
    print(mails)
    for i in mails:
        id = i['id']
        print(requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={domain}&id={id}').json())
    time.sleep(5)
    print(mails)
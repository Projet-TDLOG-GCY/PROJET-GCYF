import requests

url = 'http://127.0.0.1:5000/signup'  
data = {'id': 'clara@gmail.com', 'password': '12345'}
response = requests.post(url, data=data)

if response.status_code == 200:
    print('User added successfully')
else:
    print('Failed to add user')
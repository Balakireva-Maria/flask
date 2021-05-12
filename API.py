import requests
req = requests.get('http://127.0.0.1:5000/')
print(req.text)

resp = requests.post('http://127.0.0.1:5000/advertisment/post', json = {'header': 'Мяч', 'description': 'Продам мяч', 'owner': 'Вася' })
print(resp.json())
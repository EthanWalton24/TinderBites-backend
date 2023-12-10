import requests,json, os
from dotenv import load_dotenv

#load .env file
load_dotenv()


'''
To use api endpoints you must first register with a username and password to create an account and get your auth token, 
then you may pass your token into the other endpoints for authentication.
'''



"""register and get token"""
# data = {'username': os.getenv('USERNAME'), 'password': os.getenv('PASSWORD')}
# r = requests.post('http://127.0.0.1:8000/api/auth/register',data=data)
# token = json.loads(r.content)['token']
# print(token)


"""login and get token"""
# data = {'username': os.getenv('USERNAME'), 'password': os.getenv('PASSWORD')}
# r = requests.post('http://127.0.0.1:8000/api/auth/login',data=data)
# token = json.loads(r.content)['token']
# print(token)


"""logout"""
# r = requests.get('http://127.0.0.1:8000/api/auth/logout', headers={"Authorization": f"Token {os.getenv('TOKEN')}"})


"""list users"""
# r = requests.get('http://127.0.0.1:8000/api/list_users', headers={"Authorization": f"Token {os.getenv('TOKEN')}"})
# res = json.loads(r.content)
# print(res)


"""update address"""
# data = {'address': os.getenv('ADDRESS')}
# r = requests.put('http://127.0.0.1:8000/api/user/update/address', data=data, headers={"Authorization": f"Token {os.getenv('TOKEN')}"})
# res = json.loads(r.content)
# print(res)


"""get nearby places"""
# r = requests.get('http://127.0.0.1:8000/api/getPlaces', headers={"Authorization": f"Token {os.getenv('TOKEN')}"})
# res = json.loads(r.content)
# print(res)

"""get group places"""
r = requests.get('http://127.0.0.1:8000/api/group/get/places', headers={"Authorization": f"Token {os.getenv('TOKEN')}"})
res = json.loads(r.content)
print(res)
import requests


class UsersAPI:

    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        self.base_url = f'http://{host}:{port}'
        self.base_headers = {'Accept': 'application/json'}

    def get_all_users(self):
        response = requests.get(f'{self.base_url}/users', headers=self.base_headers)
        return response.json()

    def get_all_user_names(self):
        return [user['name'] for user in self.get_all_users()]

    def create_user(self, username: str, password: str):
        data = {'name': username, 'password': password}
        headers = self.base_headers.update({'Content-Type': 'application/json'})
        response = requests.post(f'{self.base_url}/users/create', headers=headers, json=data)
        return response.json()

    def get_user_by_name(self, username: str):
        response = requests.get(f'{self.base_url}/users/{username}', headers=self.base_headers)
        return response.json()

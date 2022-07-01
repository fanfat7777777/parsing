import requests
import os.path

users = 'fanfat7777777'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
           'Accept': 'application/vnd.github.v3+json'}

url = f'https://api.github.com/users/{users}/repos'

response = requests.get(url, headers=headers)
j_data = response.json()

# Выводим список репозиториев
for i in range(len(j_data)):
    print(j_data[i].get('full_name'))


# Запись в файл
def write_text():
    with open("j_data.json", 'w') as text:
        text.write(f'{j_data}')


if os.path.exists('j_data.json'):
    write_text()
else:
    with open("j_data.json", mode='a'):
        pass
    
    write_text()

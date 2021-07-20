from PIL import Image
from IPython.display import display
import requests as r

def get_datasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data': y[i]
            })
        return datasets
    else:
        return [
            {
                'label': labels[0],
                'data': y
            }
        ]

def set_title(title = ''):
    if title != '':
        display = 'false'
    else:
        display = 'true'
    return {
        'title': title,
        'display': display
    }

def create_chart(x, y, labels, kind = 'bar', title = ''):
    datasets = get_datasets(y, labels)
    chart = {
        'type': kind,
        'data': {
            'labels': x,
            'datasets': datasets
        }
    }
    return chart

def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content

def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)
        
def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)

url = 'http://ddragon.leagueoflegends.com/cdn/11.14.1/data/en_US/champion.json'
resp = r.get(url)
if resp.status_code == 200:
    print('A leitura do Data Dragon funcionou!')
else:
    print('A leitura do Data Dragon falhou.')
raw_data = resp.json()
champions_data = []
for value in raw_data['data'].values():
    champions_data.append([value['id'], value['tags']])
champions_data.insert(0, ['Campeão', 'Classe'])
y = [0, 0, 0, 0, 0, 0]
for i in range(1, len(champions_data)):
    if champions_data[i][1][0] == 'Assassin':
        y[0] += 1
    if champions_data[i][1][0] == 'Fighter':
        y[1] += 1
    if champions_data[i][1][0] == 'Mage':
        y[2] += 1
    if champions_data[i][1][0] == 'Marksman':
        y[3] += 1
    if champions_data[i][1][0] == 'Support':
        y[4] += 1
    if champions_data[i][1][0] == 'Tank':
        y[5] += 1
x = ['Assassino', 'Lutador', 'Mago', 'Atirador', 'Suporte', 'Tanque']
labels = ['Classe']
chart = create_chart(x, y, labels)
chart_content = get_api_chart(chart)
save_image('champions_lol.png', chart_content)
display_image('champions_lol.png')

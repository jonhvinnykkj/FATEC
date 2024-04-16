import requests

# Sua chave de API da Steam
API_KEY = '31B85073CC7BE22126DE693E7AD9EC2B'

# URL base da Steam Web API para obter informações sobre jogos em promoção
url = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'

# Fazendo a solicitação GET
response = requests.get(url)
# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Convertendo a resposta para JSON
    data = response.json()
    
    # Extraindo a lista de aplicativos (jogos)
    apps = data['applist']['apps']

    #coletanto os jogos que estão em promoção
    jogos_promocao = []
    for app in apps:
        id = app['appid']
        url = f'http://store.steampowered.com/api/appdetails?appids={id}&cc=br&l=pt'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data[str(id)]['success']:
                jogo = data[str(id)]['data']
                if 'price_overview' in jogo:
                    preco = jogo['price_overview']
                    if preco['discount_percent'] > 0:
                        jogos_promocao.append(jogo['name'])
    print(jogos_promocao)
else:
    print('Falha na solicitação')
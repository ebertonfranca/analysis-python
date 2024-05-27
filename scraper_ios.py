import pandas as pd
import numpy as np
import json

from app_store_scraper import AppStore

# Inicializa o scraper para o aplicativo VivoEasy na App Store do Brasil
vivoeasy_ios = AppStore(country='br', app_name='vivo-easy-internet-app-e-voz', app_id='1049958200')

# Extrai 5000 avaliações do aplicativo
vivoeasy_ios.review(how_many=50)

# Cria um DataFrame a partir das avaliações
vivoeasy_iosdf = pd.DataFrame(np.array(vivoeasy_ios.reviews), columns=['review'])

# Converte as colunas de 'review' para colunas individuais no DataFrame
vivoeasy_iosdf2 = vivoeasy_iosdf.join(pd.DataFrame(vivoeasy_iosdf.pop('review').tolist()))

# Exibe as primeiras linhas do DataFrame resultante
vivoeasy_iosdf2.head()

# Salva o DataFrame em um arquivo CSV
vivoeasy_iosdf2.to_csv('vivoeasy-ios-app-reviews.csv')

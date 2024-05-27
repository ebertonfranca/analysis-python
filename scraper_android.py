import pandas as pd
import numpy as np
from google_play_scraper import reviews, Sort
import matplotlib.pyplot as plt  # Certifique-se de que matplotlib está instalado

# Configurações do aplicativo
app_id = 'br.com.vivo.vivoeasy'  # ID correto do aplicativo
lang = 'pt'  # Idioma português
country = 'br'  # País Brasil

# Extrai as últimas 50 análises do aplicativo da Google Store
result, _ = reviews(
    app_id,
    lang=lang,
    country=country,
    sort=Sort.NEWEST,
    count=50
)

# Verifica se há análises extraídas
if not result:
    print("Nenhuma análise encontrada no arquivo.")
else:
    # Cria um DataFrame a partir das análises
    reviews_df = pd.DataFrame(np.array(result), columns=['review'])

    # Converte as colunas de 'review' para colunas individuais no DataFrame
    reviews_df_expanded = reviews_df.join(pd.DataFrame(reviews_df.pop('review').tolist()))

    # Exibe as primeiras linhas do DataFrame resultante
    print(reviews_df_expanded.head())

    # Salva o DataFrame em um arquivo CSV
    reviews_df_expanded.to_csv('vivoeasy-google-play-reviews.csv', index=False)
    print("Análises salvas em 'vivoeasy-google-play-reviews.csv'")
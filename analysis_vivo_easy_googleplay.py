import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

# Custom stop words list for Portuguese
custom_stop_words = set([
    'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
    'meu', 'minha', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas',
    'seu', 'sua', 'seus', 'suas', 'nosso', 'nossa', 'nossos', 'nossas',
    'deles', 'delas', 'dele', 'dela', 'um', 'uma', 'uns', 'umas',
    'de', 'a', 'o', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 'nos', 'nas',
    'por', 'para', 'com', 'sem', 'sob', 'sobre', 'entre', 'até', 'após',
    'que', 'e', 'ou', 'como', 'mas', 'porém', 'todavia', 'entretanto',
    'portanto', 'pois', 'porque', 'se', 'quando', 'enquanto', 'assim', 'então'
])

# 1. Leitura do arquivo CSV
file_path = 'vivoeasy-google-play-reviews.csv'
reviews_df = pd.read_csv(file_path)

# Certifique-se de que a coluna 'score' existe no DataFrame
if 'score' not in reviews_df.columns:
    raise KeyError("A coluna 'score' não foi encontrada no arquivo CSV.")

# 2. Classificação das análises baseadas na pontuação
positive_reviews = reviews_df[reviews_df['score'] >= 4]
negative_reviews = reviews_df[reviews_df['score'] <= 2]

# 3. Contagem de análises positivas e negativas
positive_count = len(positive_reviews)
negative_count = len(negative_reviews)
sentiment_counts = pd.Series({'positive': positive_count, 'negative': negative_count})

# 4. Análise de tópicos com categorização
def get_common_topics(reviews, custom_stop_words):
    all_words = ' '.join(reviews['content']).lower()
    words = re.findall(r'\b\w+\b', all_words)
    filtered_words = [word for word in words if word not in custom_stop_words and len(word) > 1]
    common_words = Counter(filtered_words).most_common()
    
    # Categorize common words
    categorized_words = {
        'Problemas com Pagamento': Counter(),
        'Plano e Serviços': Counter(),
        'Problemas Técnicos': Counter(),
        'Insatisfação Geral': Counter(),
        'Elogios Gerais': Counter(),
        'Plano e Benefícios': Counter(),
        'Funcionalidade e Usabilidade': Counter(),
        'Ausência de Problemas': Counter()
    }
    
    for word, count in common_words:
        if word in ['cartão', 'consigo']:
            categorized_words['Problemas com Pagamento'][word] = count
        elif word in ['plano', 'serviço']:
            categorized_words['Plano e Serviços'][word] = count
        elif word in ['aplicativo', 'app', 'mesmo']:
            categorized_words['Problemas Técnicos'][word] = count
        elif word in ['não', 'muito', 'as']:
            categorized_words['Insatisfação Geral'][word] = count
        elif word in ['muito', 'bom', 'excelente']:
            categorized_words['Elogios Gerais'][word] = count
        elif word in ['plano', 'manter', 'internet']:
            categorized_words['Plano e Benefícios'][word] = count
        elif word in ['aplicativo', 'app', 'estou']:
            categorized_words['Funcionalidade e Usabilidade'][word] = count
        elif word == 'não':
            categorized_words['Ausência de Problemas'][word] = count
            
    return categorized_words

positive_topics = get_common_topics(positive_reviews, custom_stop_words)
negative_topics = get_common_topics(negative_reviews, custom_stop_words)

# 5. Visualização dos dados
# Gráfico de pizza para a quantidade de análises positivas e negativas
plt.figure(figsize=(8, 8))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['#66b3ff','#ff9999'])
plt.title('Distribuição de Análises Positivas e Negativas')
plt.show()

# Função para plotar gráficos de barras para tópicos categorizados
def plot_topics(topics, title, color):
    for category, words in topics.items():
        if words:
            df = pd.DataFrame(words.items(), columns=['Topic', 'Count'])
            plt.figure(figsize=(10, 5))
            plt.bar(df['Topic'], df['Count'], color=color)
            plt.xlabel('Tópicos')
            plt.ylabel('Frequência')
            plt.title(f'{title} - {category}')
            plt.xticks(rotation=45)
            plt.show()

# Gráficos de barras para os tópicos mais comuns nas análises positivas e negativas
plot_topics(positive_topics, 'Top Tópicos nas Análises Positivas', 'green')
plot_topics(negative_topics, 'Top Tópicos nas Análises Negativas', 'red')

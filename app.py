# app.py

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from flask import Flask, render_template_string
import io
import base64

app = Flask(__name__)

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

# 5. Função para gerar gráficos como imagens em base64
def generate_pie_chart(data):
    fig, ax = plt.subplots()
    ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=140, colors=['#66b3ff','#ff9999'])
    ax.axis('equal')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def generate_bar_chart(topics, color):
    charts = []
    for category, words in topics.items():
        if words:
            df = pd.DataFrame(words.items(), columns=['Topic', 'Count'])
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(df['Topic'], df['Count'], color=color)
            ax.set_xlabel('Tópicos')
            ax.set_ylabel('Frequência')
            ax.set_title(category)
            ax.set_xticklabels(df['Topic'], rotation=45)
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            charts.append(base64.b64encode(img.getvalue()).decode())
            plt.close(fig)
    return charts

@app.route('/')
def index():
    pie_chart = generate_pie_chart(sentiment_counts)
    positive_charts = generate_bar_chart(positive_topics, 'green')
    negative_charts = generate_bar_chart(negative_topics, 'red')

    return render_template_string('''
        <html>
            <head><title>Review Analysis</title></head>
            <body>
                <h1>Distribuição de Análises Positivas e Negativas</h1>
                <img src="data:image/png;base64,{{ pie_chart }}" alt="Pie Chart">

                <h2>Google Play - Top Tópicos nas Análises Positivas</h2>
                {% for chart in positive_charts %}
                    <img src="data:image/png;base64,{{ chart }}" alt="Positive Topic Chart">
                {% endfor %}

                <h2>Google Play - Top Tópicos nas Análises Negativas</h2>
                {% for chart in negative_charts %}
                    <img src="data:image/png;base64,{{ chart }}" alt="Negative Topic Chart">
                {% endfor %}
            </body>
        </html>
    ''', pie_chart=pie_chart, positive_charts=positive_charts, negative_charts=negative_charts)

if __name__ == '__main__':
    app.run(debug=True)

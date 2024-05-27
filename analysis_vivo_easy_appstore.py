import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import nltk
import string
import matplotlib.pyplot as plt
import re

nltk.download('vader_lexicon')
nltk.download('stopwords')

# Load CSV file
df = pd.read_csv('vivoeasy-ios-app-reviews.csv')

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()

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

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    tokens = text.split()
    tokens = [word for word in tokens if word not in custom_stop_words]
    return ' '.join(tokens)

# Apply preprocessing to each review
df['cleaned_review'] = df['review'].apply(preprocess_text)

# Classify reviews based on rating
positive_reviews = df[df['rating'] >= 4]
negative_reviews = df[df['rating'] <= 3]

# Count sentiments
positive_count = positive_reviews.shape[0]
negative_count = negative_reviews.shape[0]

# Print counts
print(f'Análises positivas: {positive_count}')
print(f'Análises negativas: {negative_count}')

# Extract themes from reviews with categorization
def get_common_topics(reviews, custom_stop_words):
    all_words = ' '.join(reviews).lower()
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

positive_topics = get_common_topics(positive_reviews['cleaned_review'], custom_stop_words)
negative_topics = get_common_topics(negative_reviews['cleaned_review'], custom_stop_words)

# Visualization
# Gráfico de pizza para a quantidade de análises positivas e negativas
labels = ['Positivas', 'Negativas']
sizes = [positive_count, negative_count]
colors = ['#66b3ff', '#ff6666']
explode = (0.1, 0)  # explode the 1st slice

plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('IOS - Análise de sentimento de avaliações de clientes')
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
plot_topics(positive_topics, 'AppStore - Top Tópicos de Análises Positivas', 'green')
plot_topics(negative_topics, 'AppStore - Top Tópicos de Análises Negativas', 'red')

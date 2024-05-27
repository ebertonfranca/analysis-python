import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import nltk
import string
import matplotlib.pyplot as plt

nltk.download('vader_lexicon')
nltk.download('stopwords')

# Load CSV file
df = pd.read_csv('vivoeasy-ios-app-reviews.csv')

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    tokens = text.split()
    stop_words = set(stopwords.words('portuguese'))
    tokens = [word for word in tokens if word not in stop_words]
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

# Extract themes from negative reviews
negative_reviews_text = negative_reviews['cleaned_review']
vectorizer = CountVectorizer(max_features=10)
X = vectorizer.fit_transform(negative_reviews_text)
theme_counts = X.toarray().sum(axis=0)
themes = vectorizer.get_feature_names_out()

# Print top negative review themes
theme_freq = dict(zip(themes, theme_counts))
top_themes = sorted(theme_freq.items(), key=lambda item: item[1], reverse=True)

print('Top frequency negative review themes:')
for theme, freq in top_themes:
    print(f'{theme}: {freq}')

# Visualization
labels = ['Positivas', 'Negativas']
sizes = [positive_count, negative_count]
colors = ['#66b3ff', '#ff6666']
explode = (0.1, 0)  # explode the 1st slice

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('IOS - Análise de sentimento de avaliações de clientes')
plt.show()

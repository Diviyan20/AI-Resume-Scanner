import re
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')


def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    #Remove special characters and digits using regular expressions
    text = re.sub(r'/d+', '', text) #Removes digits
    text = re.sub(r'[^\w\s]', '', text ) #Removes special characters

    #Tokenize the text
    tokens = nltk.word_tokenize(text)
    
    return tokens

# Remove stopwords (eg. "the", "is", "and")
def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

# Perform Lemmatization for consolidating words
def perform_lemmatization(tokens):
    lemmatizer = nltk.WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

def clean_text(text):
    tokens = preprocess_text(text)
    filterd_words = remove_stopwords(tokens)
    lemmatized_tokens = perform_lemmatization(filterd_words)
    clean_text = ' '.join(lemmatized_tokens)
    return clean_text
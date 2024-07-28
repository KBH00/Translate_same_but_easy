import textstat
import nltk
from nltk.corpus import wordnet
from collections import Counter

nltk.download('brown')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

word_freq = Counter(nltk.corpus.brown.words())

total_words = sum(word_freq.values())
word_complexity = {word: (total_words / freq) for word, freq in word_freq.items()}

def get_word_complexity(word):
    return word_complexity.get(word.lower(), total_words) 

def get_readability_level(text):
    readability_score = textstat.flesch_kincaid_grade(text)
    if readability_score <= 5:
        return 1
    elif readability_score <= 8:
        return 2
    else:
        return 3


from transformers import pipeline
from huggingface_hub import login

import nltk

nltk.download('punkt')

def identify_complex_words(text, model, threshold=0.9):
    words = nltk.word_tokenize(text)
    complex_words = []

    for word in words:
        masked_text = text.replace(word, '[MASK]')
        predictions = model(masked_text)
        if any(pred['token_str'] == word and pred['score'] < threshold for pred in predictions):
            complex_words.append(word)

    return complex_words

unmasker = pipeline('fill-mask', model='meta-llama/Llama-2-7b-chat-hf')

def get_contextual_synonym(word, context, model, increase_complexity=True):
    masked_text = context.replace(word, '[MASK]')
    predictions = model(masked_text)
    
    predictions = sorted(predictions, key=lambda x: len(x['token_str']), reverse=increase_complexity)
    
    for pred in predictions:
        synonym = pred['token_str']
        if synonym != word:
            return synonym

    return word  # Return the original word if no synonym is found

def replace_words(text, words_to_change, model, increase_complexity=True):
    words = nltk.word_tokenize(text)
    new_words = []

    for word in words:
        if word in words_to_change:
            new_word = get_contextual_synonym(word, text, model, increase_complexity)
            new_words.append(new_word)
        else:
            new_words.append(word)

    return ' '.join(new_words)


def adjust_text_complexity(text, target_level, model):
    current_level = get_readability_level(text)  # Assume this function is defined as before
    words_to_change = identify_complex_words(text, model)
    print(words_to_change)
    increase_complexity = target_level > current_level
    new_text = replace_words(text, words_to_change, model, increase_complexity)
    return new_text

input_text = "I want to buy medical imaging"
target_level = 1
new_text = adjust_text_complexity(input_text, target_level, unmasker)
print(f"Original text: {input_text}")
print(f"New text: {new_text}")


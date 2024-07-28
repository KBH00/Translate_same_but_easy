import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import cmudict

def check_nltk_data(package):
    try:
        nltk.data.find(package)
        return True
    except LookupError:
        return False

if not check_nltk_data('tokenizers/punkt'):
    nltk.download('punkt')

if not check_nltk_data('corpora/cmudict.zip'):
    nltk.download('cmudict')

d = cmudict.dict()

def syllable_count(word):
    if word.lower() in d:
        return len([phoneme for phoneme in d[word.lower()][0] if phoneme[-1].isdigit()])
    else:
        return len([char for char in word if char in 'aeiouy'])

def flesch_kincaid_grade(words, sentences, syllables):
    return 0.39 * (len(words) / len(sentences)) + 11.8 * (syllables / len(words)) - 15.59

def gunning_fog(words, sentences, complex_words):
    return 0.4 * ((len(words) / len(sentences)) + 100 * (complex_words / len(words)))

def smog_grade(sentences, polysyllabic_words):
    return 1.0430 * (30 * (polysyllabic_words / len(sentences)))**0.5 + 3.1291

def ari(words, sentences, characters):
    return 4.71 * (characters / len(words)) + 0.5 * (len(words) / len(sentences)) - 21.43

def coleman_liau_index(words, sentences, characters):
    L = (characters / len(words)) * 100
    S = (len(sentences) / len(words)) * 100
    return 0.0588 * L - 0.296 * S - 15.8

def dale_chall_readability_score(words, sentences, difficult_words):
    score = 0.1579 * (difficult_words / len(words) * 100) + 0.0496 * (len(words) / len(sentences))
    if (difficult_words / len(words)) > 0.05:
        score += 3.6365
    return score

def count_complex_words(words):
    return sum(1 for word in words if syllable_count(word) >= 3)

def count_polysyllabic_words(words):
    return sum(1 for word in words if syllable_count(word) >= 3)

def count_difficult_words(words, easy_word_list):
    return sum(1 for word in words if word.lower() not in easy_word_list)

easy_words = set()  # Add list of easy words here

def convert_to_grade_level(score, conversion_table):
    for threshold, grade in conversion_table:
        if score <= threshold:
            return grade
    return conversion_table[-1][1]

def calculate_readability(text):
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    syllables = sum(syllable_count(word) for word in words)
    characters = sum(len(word) for word in words)
    complex_words = count_complex_words(words)
    polysyllabic_words = count_polysyllabic_words(words)
    difficult_words = count_difficult_words(words, easy_words)
    
    fk_grade = flesch_kincaid_grade(words, sentences, syllables)
    gf_index = gunning_fog(words, sentences, complex_words)
    smog = smog_grade(sentences, polysyllabic_words)
    ari_score = ari(words, sentences, characters)
    cli_index = coleman_liau_index(words, sentences, characters)
    dc_score = dale_chall_readability_score(words, sentences, difficult_words)
    
    fk_grade_level = convert_to_grade_level(fk_grade, [(4.9, 4), (5.9, 6), (6.9, 8), (7.9, 10), (8.9, 12), (9.9, 15), (10, 16)])
    gf_grade_level = convert_to_grade_level(gf_index, [(6, 6), (8, 8), (10, 10), (12, 12), (14, 14), (16, 16), (18, 18)])
    smog_grade_level = convert_to_grade_level(smog, [(4.9, 4), (5.9, 6), (6.9, 8), (7.9, 10), (8.9, 12), (9.9, 15), (10, 16)])
    ari_grade_level = convert_to_grade_level(ari_score, [(5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)])
    cli_grade_level = convert_to_grade_level(cli_index, [(5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)])
    dc_grade_level = convert_to_grade_level(dc_score, [(4.9, 4), (5.9, 6), (6.9, 8), (7.9, 10), (8.9, 12), (9.9, 15), (10, 16)])
    
    average_grade_level = (fk_grade_level + gf_grade_level + smog_grade_level + ari_grade_level + cli_grade_level + dc_grade_level) / 6
    return {
        "Flesch-Kincaid": fk_grade_level,
        "Gunning Fog": gf_grade_level,
        "SMOG": smog_grade_level,
        "ARI": ari_grade_level,
        "Coleman-Liau": cli_grade_level,
        "Dale-Chall": dc_grade_level,
        "Average Grade Level": average_grade_level
    }

# Example text
text = "They designed it to correct certain shortcomings in the Flesch Reading Ease Formula."
def avg_readability(text):
    readability_scores = calculate_readability(text)
    for formula, score in readability_scores.items():
        print(f"{formula}: {score}")
avg_readability(text)

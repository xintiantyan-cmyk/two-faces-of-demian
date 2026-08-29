from nltk.tokenize import sent_tokenize, regexp_tokenize

# Functions for text analysis.
# Features: 
# - average sentence length
# - puncuation rates (count per 100 words), 
# - type-token ratio (TTR) 
# - function word distribution 
# - paragraph-to-sentence ratio

def avg_sentence_length(text: str) -> float:
    """Calculate the average sentence length in words. The input text should be a pre-cleaned chunk of text.
    Note that words like "don't" and "it's" are counted as single words, while hyphenated words like "well-being" are counted as two words.
    Formula: average sentence length = total number of words / total number of sentences
    """
    sentences = sent_tokenize(text)  
    sentence_num = len(sentences)
    words = regexp_tokenize(text, r"\b\w+(?:'\w+)?\b", gaps=False)

    if sentence_num > 0:
        return len(words) / sentence_num
    else:
        return 0.0

def punctuation_count(text: str) -> dict[str, int]:
    """Count the number of punctuation marks in the text."""
    punctuation_marks = ['.', ',', '!', '?', ';', ':', '"', "'", "...", "--"]
    result = {}
    for punctuation in punctuation_marks:
        count = text.count(punctuation)
        result[punctuation] = count
    return result

def punctuation_rate_per_1000_words(text:str) -> dict[str, float]:
    """Calculate the rate of punctuation marks per 1000 words in the text."""
    punctuation_counts = punctuation_count(text)
    words = regexp_tokenize(text, r"\b\w+(?:'\w+)?\b", gaps=False)
    word_count = len(words)

    if word_count == 0:
        return {punctuation: 0.0 for punctuation in punctuation_counts}

    punctuation_rates = {}

    for punctuation, count in punctuation_counts.items():
        punctuation_rates[punctuation] = (count / word_count) * 1000
    return punctuation_rates

def typeTokenRatio(text: str) -> float:
    """Calculate the type-token ratio (TTR) of the text. The input text should be a pre-cleaned chunk of text.
    Formula: TTR = number of unique words / total number of words
    """
    words = regexp_tokenize(text, r"\b\w+(?:'\w+)?\b", gaps=False)
    return len(set(words)) / len(words)

def function_word_distribution(text: str) -> float:
    """Calculate the Relative frequency of function words in the text. The input text should be a pre-cleaned text.
    Formula: Relative frequency of function words = number of function words / total number of words
    """
    function_words = """a between in nor some upon
    about both including nothing somebody us
    above but inside of someone used
    after by into off something via
    all can is on such we
    although fucos it once than what
    am do its one that whatever
    among down latter onto the when
    an each less opposite their where
    and either like or them whether
    another enough little our these which
    any every lots outside they while
    anybody everybody many over this who
    anyone everyone me own those whoever
    anything everything more past though whom
    are few most per through whose
    around following much plenty till will
    as for must plus to with
    at from my regarding toward within
    be have near same towards without
    because he need several under worth
    before her neither she unless would
    behind him no should unlike yes
    below i nobody since until you
    beside if none so up your
    """
    function_words_list = function_words.split()
    words = regexp_tokenize(text, r"\b\w+(?:'\w+)?\b", gaps=False)
    count = 0

    for word in words:
        if word.lower() in function_words_list:
            count += 1

    if len(words) == 0:
        return 0.0
    return count / len(words) 

def paragraph_to_sentence_ratio(text: str, paragraph_num: int) -> float:
    """Calculate the paragraph-to-sentence ratio of the text. The input text should be a pre-cleaned chunk of text.
    Formula: paragraph-to-sentence-ration = number of sentences / number of paragraphs 
    """
    sentences = sent_tokenize(text)  
    if paragraph_num > 0:
        return len(sentences) / paragraph_num
    else:
        return 0.0

import nltk
from nltk.tokenize import sent_tokenize, regexp_tokenize, word_tokenize
from collections import Counter

nltk.download('punkt_tab', quiet=True)
nltk.download('punkt')

# Functions for text analysis.
# Features: 
# - average sentence length
# - puncuation rates (count per 100 words), 
# - type-token ratio (TTR) 
# - function word distribution 
# - paragraph-to-sentence ratio (number of sentences per paragraph)

def avg_sentence_length(text: str) -> float:
    """Calculate the average sentence length in words. The input text should be a pre-cleaned chunk of text.
    Note that words like "don't" and "it's" are counted as single words, while hyphenated words like "well-being" are counted as two words.
    Formula: average sentence length = total number of words / total number of sentences
    """
    sentences = _tokenize_sentences(text)  
    sentence_num = len(sentences)
    words = _extract_words(text)

    if sentence_num > 0:
        return len(words) / sentence_num
    else:
        return 0.0

def _punctuation_count(text: str) -> dict[str, int]:
    """Count the number of punctuation marks in the text."""
    # punctuation_marks = ['.', ',', '!', '?', ';', ':', '"', "'", "...", "--"]
    TARGET_PUNCTUATIONS = ['.', ',', '!', '?', ';', ':', '"', "'", '...', '--']

    tokens = word_tokenize(text)
    
    filtered_tokens = []
    for token in tokens:
        # Standardize NLTK open/close double quotes
        if token == "''" or token == "``" or token == "“" or token == "”":
            filtered_tokens.append('"')
        # Standardize curly single quotes/apostrophes
        elif token == "’" or token == "‘":
            filtered_tokens.append("'")
        # Handle em-dash and en-dash and different formatting of dashes
        elif token == "-" or token == "----" or token == "—" or token == "–":
            filtered_tokens.append("--")
        elif token == "...":
            filtered_tokens.append("...")
        elif token in TARGET_PUNCTUATIONS:
            filtered_tokens.append(token)

    punctuations = {}
    for punctuation in TARGET_PUNCTUATIONS:
        punctuations[punctuation] = 0

    actual_punctuations = Counter(filtered_tokens)
    for punc, count in actual_punctuations.items():
        punctuations[punc] = count

    return punctuations

def punctuation_rate_per_1000_words(text:str) -> dict[str, float]:
    """Calculate the rate of punctuation marks per 1000 words in the text."""
    punctuation_counts = _punctuation_count(text)
    words = _extract_words(text)
    word_count = len(words)

    PUNCTUATION_LABEL_MAP = {
        '.': 'Period',
        ',': 'Comma',
        '!': 'Exclamation',
        '?': 'Question',
        ';': 'Semicolon',
        ':': 'Colon',
        '"': 'DoubleQuote',
        "'": 'SingleQuote',
        '...': 'Ellipsis',
        '--': 'Dash'
    }
    print(f"Word count: {word_count}")

    punctuation_rates = {}

    if word_count == 0:
        for symbol in punctuation_counts:
            label = PUNCTUATION_LABEL_MAP.get(symbol, symbol)
            column_name = "Punctuation_Rate_" + label
            punctuation_rates[column_name] = 0.0
        return punctuation_rates

    for punctuation, count in punctuation_counts.items():
        label = PUNCTUATION_LABEL_MAP.get(punctuation, punctuation)
        punctuation_rates["Punctuation_Rate_" + label] = (count / word_count) * 1000
    return punctuation_rates

def type_token_ratio(text: str) -> float:
    """Calculate the type-token ratio (TTR) of the text. The input text should be a pre-cleaned chunk of text.
    Formula: TTR = number of unique words / total number of words
    """
    words = _extract_words(text)

    if len(words) == 0:
        return 0.0
    cleaned_words  = []

    for word in words:
        cleaned_word = word.lower()
        cleaned_words.append(cleaned_word)
    return len(set(cleaned_words)) / len(cleaned_words)

def function_word_distribution(text: str) -> dict[str, float]:
    """Calculate the Relative frequency of function words in the text. The input text should be a pre-cleaned text.
    Formula: Relative frequency of function words = number of function words / total number of words
    """
    function_words = """a between in nor some upon
    about both including nothing somebody us
    above but inside of someone used
    after by into off something via
    all can is on such we
    although it once than what
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
    words = _extract_words(text)
    total = len(words)
    if total == 0:
        return {f"Function_Word_Freq_{word}": 0.0 for word in sorted(set(function_words_list))}

    counts = Counter(word.lower() for word in words if word.lower() in function_words_list)
    return {f"Function_Word_Freq_{word}": counts[word] / total for word in sorted(set(function_words_list))}

def paragraph_to_sentence_ratio(text: str, paragraph_num: int) -> float:
    """Calculate the paragraph-to-sentence ratio of the text. The input text should be a pre-cleaned chunk of text.
    Formula: paragraph-to-sentence-ratio = number of sentences / number of paragraphs 
    """
    sentences = _tokenize_sentences(text)  
    if paragraph_num > 0:
        return len(sentences) / paragraph_num
    else:
        return 0.0

def _tokenize_sentences(text: str) -> list[str]:
    """Splits cleaned text into sentences paragraph by paragraph"""
    sentences = []
    # Split by double newlines so sentence boundaries aren't broken by line wraps
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    
    for paragraph in paragraphs:
        # Replace intra-paragraph single newlines with spaces before tokenizing
        clean_para = " ".join(paragraph.splitlines())
        sentences.extend(sent_tokenize(clean_para))
        
    return sentences

def _extract_words(text: str) -> list[str]:
    """Helper to maintain consistent word tokenization across all metrics."""
    return regexp_tokenize(text, r"\b\w+(?:['’]\w+)?\b", gaps=False)

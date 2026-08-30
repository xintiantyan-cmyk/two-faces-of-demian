import core.stylometry as stylometry
import pandas as pd
import regex as re

def analyze_text(text: str, paragraph_num: int) -> dict:
    """Analyze the text and return a dictionary of stylometric features."""
    analysis_results = {
        "Average_Sentence_Length": stylometry.avg_sentence_length(text),
        "Punctuation_Rate_per_1000_Words": stylometry.punctuation_rate_per_1000_words(text),
        "Type_Token_Ratio": stylometry.typeTokenRatio(text),
        "Function_Word_Distribution": stylometry.function_word_distribution(text),
        "Paragraph_to_Sentence_Ratio": stylometry.paragraph_to_sentence_ratio(text, paragraph_num)
    }
    return analysis_results

def _split_text_by_chapter(text: str) -> list[str]:
    """Split the text into a list of chunks by chapter. Chapter headings are deleted in the process."""
    number_words = r'(?:ZERO|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|ELEVEN|TWELVE|THIRTEEN|FOURTEEN|FIFTEEN|SIXTEEN|SEVENTEEN|EIGHTEEN|NINETEEN|TWENTY)'
    header_regex = rf'(?:\r?\n)+(?:CHAPTER|Chapter)\s+(?:[0-9]+|[IVXLCDM]+|{number_words})'

    raw_chapters = re.split(header_regex, text, flags=re.IGNORECASE)
    chapters = [c.strip() for c in raw_chapters if c.strip()]
    return chapters

# def compare_chapters(text1: str, text2: str) -> pd.DataFrame:
#     """Compares the stylometric features of the given two texts. Results are returned as a Pandas DataFrame."""
#     result1 = analyze_text(text1.strip(), _count_paragraphs(text1))
#     result2 = analyze_text(text2.strip(), _count_paragraphs(text2))

#     text1_metrics = result1.copy()
#     text1_metrics["Chapter"] = "Chapter 1"

#     text2_metrics = result2.copy()
#     text2_metrics["Chapter"] = "Chapter 2"

#     comparison_df = pd.DataFrame([text1_metrics, text2_metrics])
#     return comparison_df

def _count_paragraphs(text: str) -> int:
    """Counts the number of paragraphs in the given text."""
    if text.strip() == "":
        return 0
    raw_paragraphs = text.split("\n\n")
    paragraphs = [p for p in raw_paragraphs if p.strip()]
    return len(paragraphs)

def analyze_book(text: str, title: str, author: str, published_year: int, translator: str, translation_year: int, has_chap_0: bool) -> pd.DataFrame:
    """Analyzes the given book text and returns a DataFrame with stylometric features for each chapter."""
    chapters = _split_text_by_chapter(text)
    chapter_results = []

    for idx, chapter in enumerate(chapters):
        cleaned_chapter = chapter.strip() # Safe gaurd 
        if cleaned_chapter:
            result = analyze_text(cleaned_chapter, _count_paragraphs(chapter))
            if has_chap_0:
                result["Chapter"] = f"Chapter {idx}"
            else:
                result["Chapter"] = f"Chapter {idx + 1}"
            result["Title"] = title
            result["Author"] = author
            result["Published_Year"] = published_year
            result["Translator"] = translator
            result["Translation_Year"] = translation_year
            chapter_results.append(result)

    df = pd.DataFrame(chapter_results)
    df.set_index(["Title", "Author", "Published_Year", "Translator", "Translation_Year", "Chapter"], inplace=True)

    # # Create a DataFrame from the chapter results where each row corresponds to a chapter and each column corresponds to a stylometric feature.
    # df = pd.DataFrame.from_dict(chapter_results, orient="index") 

    # multi_index_tuples = [(title, author, published_year, translator, translation_year, chapter) for chapter in df.index]
    # multi_index_df = pd.MultiIndex.from_tuples(multi_index_tuples, names=["Title", "Author", "Published_Year", "Translator", "Translation_Year", "Chapter"])
    # df.index = multi_index_df
    return df
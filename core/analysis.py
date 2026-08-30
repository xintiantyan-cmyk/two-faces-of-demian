import core.stylometry as stylometry
import pandas as pd
import regex as re

def _analyze_text(text: str, paragraph_num: int) -> dict:
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
    header_pattern = rf'(?:\r?\n|^)\s*(?:CHAPTER|Chapter)\s+(?:[0-9]+|[IVXLCDM]+|{number_words})[^\r\n]*'

    # Find the start positions of all chapter headings
    matches = list(re.finditer(header_pattern, text, flags=re.IGNORECASE))
    
    if not matches:
        return [text.strip()]

    chapters = []
    for i in range(len(matches)):
        start_pos = matches[i].end()  # Start AFTER the heading text
        
        # If it's the last chapter, read to the end of the text; otherwise, read up to the next match
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(text)
            
        chapter_content = text[start_pos:end_pos].strip()
        if chapter_content:
            chapters.append(chapter_content)

    return chapters

def _count_paragraphs(text: str) -> int:
    """Counts the number of paragraphs in the given text."""
    if text.strip() == "":
        return 0
    raw_paragraphs = text.split("\n\n")
    paragraphs = [p for p in raw_paragraphs if p.strip()]
    print(len(paragraphs))
    return len(paragraphs)

def analyze_book(text: str, title: str, author: str, published_year: int, translator: str, translation_year: int, has_chap_0: bool) -> pd.DataFrame:
    """Analyzes the given book text and returns a DataFrame with stylometric features for each chapter."""
    chapters = _split_text_by_chapter(text)
    chapter_results = []

    for idx, chapter in enumerate(chapters):
        cleaned_chapter = chapter.strip() # Safe gaurd 
        if cleaned_chapter:
            result = _analyze_text(cleaned_chapter, _count_paragraphs(chapter))
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

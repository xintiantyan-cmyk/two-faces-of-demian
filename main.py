import core.analysis as analysis
from data_access.data_writer import save_book_profile
from data_access.text_loader import TextLoader

if __name__ == "__main__":
    # Load the pre-cleaned text file
    text_loader = TextLoader("data/raw/Demian-Priday-cleaned.txt")
    book_text = text_loader.load_text()

    # Analyze the book and get the stylometric features for each chapter
    book_profile_df = analysis.analyze_book(
        book_text,
        "Demian: The Story of Emil Sinclair's Youth",
        "Hermann Hesse",
        1919,
        "N. H. Priday",
        1923,
        True
    )

    # Save the book profile
    save_book_profile(book_profile_df, "data/processed/Demian-Priday.csv")

    text_loader = TextLoader("data/raw/Demian-Searls-cleaned.txt")
    book_text_2 = text_loader.load_text()

    book_profile_df_2 = analysis.analyze_book(
            book_text_2,
            "Demian: The Story of Emil Sinclair's Youth",
            "Hermann Hesse",
            1919,
            "Damion Searls",
            2013,
            True
        )

    save_book_profile(book_profile_df_2, "data/processed/Demian-Searls.csv")

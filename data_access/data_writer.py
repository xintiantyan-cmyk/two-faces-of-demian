import pandas as pd
from pathlib import Path

# Writes the book profile to a CSV file. 
# The book profile is a Pandas DataFrame with stylometric features for each chapter of the book.

def save_book_profile(df: pd.DataFrame, filepath: str) -> None:
    """Writes the book profile DataFrame to a CSV file at the specified filepath."""
    path = Path(filepath)
    #create the parent directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)

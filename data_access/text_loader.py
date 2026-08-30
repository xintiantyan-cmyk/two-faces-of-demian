from pathlib import Path
import re

class TextLoader:
    """Reads a pre-cleaned text file from disk.
    
    Attributes:
        file_path (Path): The path to the text file.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def _preprocess_text(self, text: str) -> str:
        """Preprocesses text by normalizing line breaks, stripping tab indentations,
        and standardizing spaced ellipses so all metrics evaluate identical text. 
        The orginal text is not modified. 
        """
        # Normalize spaced ellipses like ". . ." to "..."
        result = re.sub(r'\.\s*\.\s*\.', '...', text)

        raw_paragraphs = result.split("\n\n")
        cleaned_paragraphs = []

        for paragraph in raw_paragraphs:
        # Strip leading/trailing tabs & spaces per line within the paragraph
            lines = [line.strip() for line in paragraph.splitlines() if line.strip()]
            if lines:
                # Rejoin intra-paragraph wrapped lines with a single space or single newline
                cleaned_paragraphs.append("\n".join(lines))

        # Join separate paragraphs with double newlines
        return "\n\n".join(cleaned_paragraphs)

    def load_text(self) -> str:
        if not self.file_path.exists():
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")
        if not self.file_path.is_file():
            raise ValueError(f"The path {self.file_path} is not a file.")
        with self.file_path.open('r', encoding='utf-8') as file:
            raw_text = file.read().strip()
            return self._preprocess_text(raw_text)

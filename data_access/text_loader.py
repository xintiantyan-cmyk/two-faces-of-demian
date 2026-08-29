from pathlib import Path

class TextLoader:
    """Reads a pre-cleaned text file from disk.
    
    Attributes:
        file_path (Path): The path to the text file.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load_text(self) -> str:
        if not self.file_path.exists():
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")
        if not self.file_path.is_file():
            raise ValueError(f"The path {self.file_path} is not a file.")
        with self.file_path.open('r', encoding='utf-8') as file:
            return file.read().strip()

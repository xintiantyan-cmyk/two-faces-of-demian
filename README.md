<div align="center">

# 🎭 Two Faces of Demian

A stylometric comparison of two English translations of Hermann Hesse's _Demian_ — from raw text to interactive visualizations.

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](http://makeapullrequest.com)
[![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square)](https://www.python.org)

</div>

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [The Book & The Two Translations](#-the-book--the-two-translations)
- [How the Analysis Works](#-how-the-analysis-works)
- [Stylometric Features](#-stylometric-features)
- [Using the Dashboard](#-using-the-dashboard)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Dashboard Views](#-dashboard-views)
- [Limitations & Roadmap](#-limitations--roadmap)
- [Credits](#-credits)

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/xintiantyan-cmyk/two-faces-of-demian.git
cd two-faces-of-demian

# 2. Create & activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install pandas nltk regex streamlit altair

# 4. Run the analysis (writes data/processed/*.csv)
python main.py

# 5. Launch the interactive dashboard
streamlit run data_access/visualizer.py
```

The dashboard opens in your browser — compare the two translations side-by-side.

---

## ✨ Features

- **Two-translation comparison** — N. H. Priday (1923) vs. Damion Searls (2013): the same German novel through two translators' lenses.
- **Chapter-level granularity** — Every metric is computed per chapter, not just book-wide.
- **Five stylometric dimensions** — vocabulary richness, pacing, paragraph structure, punctuation, and function-word distribution.
- **Interactive dashboard** — Filter by chapter, toggle normalization, and compare translations with Streamlit.
- **Consistent preprocessing** — Normalizes line breaks, tab indentation, and spaced ellipses so both texts are measured identically.
- **Zero manual annotation** — Pure surface-level statistics; no part-of-speech tagging or semantic analysis.

---

## 📖 The Book & The Two Translations

**Demian: The Story of Emil Sinclair's Youth** (1919) is Hermann Hesse's coming-of-age novel about Emil Sinclair's journey from a sheltered childhood into a world of duality — good and evil, light and dark — guided by the enigmatic Max Demian.

| Translation | Translator    | Year | Era / Publisher       |
| ----------- | ------------- | ---- | --------------------- |
| **Priday**  | N. H. Priday  | 1923 | First English edition |
| **Searls**  | Damion Searls | 2013 | Penguin Classics      |

<details>
<summary><b>📚 Chapter structure</b></summary>

Both cleaned texts are split into **9 segments** — a prologue (`Chapter 0`) followed by 8 numbered chapters. The chapter-splitting regex recognizes headings written as `CHAPTER` or `Chapter`, followed by Arabic numerals, Roman numerals, or number words.

</details>

---

## 🔬 How the Analysis Works

The pipeline processes each translation through four stages:

| Stage                     | What It Does                                                                                                                               |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Load & preprocess**  | `TextLoader` reads the cleaned `.txt`, normalizes line breaks, strips tab indentation, and standardizes spaced ellipses (`. . .` → `...`). |
| **2. Chapter split**      | Regex locates chapter headings and slices the text into per-chapter chunks (headings are discarded).                                       |
| **3. Feature extraction** | `_analyze_text` computes TTR, sentence length, paragraph ratio, 10 punctuation rates, and ~150 function-word frequencies per chapter.      |
| **4. Export**             | `analyze_book` builds a multi-indexed DataFrame; `save_book_profile` writes it to `data/processed/*.csv`.                                  |

---

## 📊 Stylometric Features

| Feature                         | What It Measures                         | Formula                            |
| ------------------------------- | ---------------------------------------- | ---------------------------------- |
| **Type-Token Ratio (TTR)**      | Vocabulary richness                      | unique words ÷ total words         |
| **Average Sentence Length**     | Pacing / syntactic complexity            | total words ÷ total sentences      |
| **Paragraph-to-Sentence Ratio** | Sentence density per paragraph           | total sentences ÷ total paragraphs |
| **Punctuation Rates**           | Stylistic punctuation habits (10 marks)  | (count ÷ total words) × 1000       |
| **Function-Word Distribution**  | The translator's stylistic "fingerprint" | function-word count ÷ total words  |

> **Punctuation marks tracked:** period, comma, exclamation, question, semicolon, colon, double quote, single quote, ellipsis, and dash.
>
> **Function words:** ~150 common words (articles, pronouns, prepositions, conjunctions, auxiliaries) — words that carry grammar rather than meaning, making them stable markers of style.

---

## 🖥️ Using the Dashboard

1. **Launch it** — `streamlit run data_access/visualizer.py`.

| Dashboard Section              | Chart Type   | What It Shows                                      |
| ------------------------------ | ------------ | -------------------------------------------------- |
| **Vocabulary & Structure**     | Grouped bars | Type-Token Ratio + Paragraph-to-Sentence Ratio     |
| **Pacing**                     | Line         | Average Sentence Length per chapter                |
| **Punctuation Frequencies**    | Stacked bars | 10 punctuation marks (optional 100% normalization) |
| **Function Word Distribution** | Stacked bars | ~150 function words (optional 100% normalization)  |

2. **Pick chapters** — Use the multi-select above each section to include or exclude chapters.
3. **Compare translations** — Priday and Searls appear side-by-side as distinct colors in every chart.
4. **Toggle normalization** — For punctuation and function words, switch between raw counts and 100% proportions.
5. **Rank function words** — Choose by per-translation rank or global rank; the top 5 are pre-selected.

---

## 🛠️ Tech Stack

| Layer         | Tech                                  |
| ------------- | ------------------------------------- |
| Analysis      | Python 3, NLTK (tokenization), pandas |
| Regex         | `regex` (enhanced `re` drop-in)       |
| Visualization | Streamlit                             |
| Storage       | CSV via pandas DataFrame export       |

---

## 📁 Project Structure

```
two-faces-of-demian/
├── core/                 # Stylometric analysis logic
│   ├── analysis.py       # Chapter split, feature orchestration, DataFrame build
│   └── stylometry.py     # Individual metrics (TTR, sentence length, punctuation, function words)
├── data_access/          # I/O and visualization
│   ├── text_loader.py    # TextLoader: read + preprocess raw text
│   ├── data_writer.py    # save_book_profile: DataFrame → CSV
│   └── visualizer.py     # Streamlit dashboard (Altair charts)
├── data/
│   ├── raw/              # Pre-cleaned .txt files (gitignored — copyrighted)
│   └── processed/        # Per-chapter feature CSVs (analysis output)
├── main.py               # Entry point: load → analyze → save both translations
└── requirements.txt      # Project dependencies
```

---

## 📦 Installation

<details>
<summary><b>Prerequisites & Full Setup</b></summary>

- Python 3.10+

```bash
git clone https://github.com/xintiantyan-cmyk/two-faces-of-demian.git
cd two-faces-of-demian

# Create & activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install pandas nltk regex streamlit altair
```

> NLTK's `punkt` tokenizer data is downloaded automatically on first import (`core/stylometry.py`).

### Adding your own texts

Raw text files are gitignored for copyright reasons. Drop your own pre-cleaned `.txt` files into `data/raw/`, update the paths and metadata in `main.py` to match, then run `python main.py` to regenerate the profiles.

</details>

---

## 📈 Sample Dashboard Views

---

## ⚠️ Limitations & Roadmap

### Known Limitations

- **Surface-level metrics only** — No syntax/dependency parsing, part-of-speech tagging, or semantic analysis.
- **Visual comparison only** — No statistical significance testing (e.g., p-values or permutation tests).
- **English only** — The analysis targets the two English translations; the German original is not included.
- **Raw text excluded** — `data/raw/*.txt` is gitignored, so reproduction requires supplying the texts yourself.
- **Time gap between translations** - Differences in basic stylometric features listed might be due to differences in historical translation conventions and language conventions rather than personal translation style.

### Roadmap

- Add the German original (1919) for a three-way comparison.
- Add more translations (e.g., W. J. Strachan 1958; Michael Roloff & Michael Lebeck 1965).
- Add statistical tests on function-word and punctuation differences.
- Extend features: mean word length, moving-average TTR (MATTR), and n-gram frequencies.

---

## 📜 Credits

- **Novel:** Hermann Hesse, _Demian: The Story of Emil Sinclair's Youth_ (1919).
- **Translations:** N. H. Priday (1923); Damion Searls (2013, Penguin Classics).
- **Tokenization:** [NLTK](https://www.nltk.org/).
- **Visualization:** [Streamlit](https://streamlit.io) + [Altair](https://altair-viz.github.io/).

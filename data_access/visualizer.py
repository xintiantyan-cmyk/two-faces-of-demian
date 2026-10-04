from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

CHAPTER_COL = "Chapter"
TRANSLATION_COL = "Translation"

ROOT = Path(__file__).resolve().parents[1]
CSV_A = ROOT / "data" / "processed" / "Demian-Priday.csv"
CSV_B = ROOT / "data" / "processed" / "Demian-Searls.csv"


class TranslationData:
    """Loads and reshapes the two translation profile CSVs into chart-ready form."""

    def __init__(self, csv_a, csv_b, label_a="Priday (1923)", label_b="Searls (2013)"):
        self.csv_a = csv_a
        self.csv_b = csv_b
        self.label_a = label_a
        self.label_b = label_b

    def _read_profile(self, path, label):
        df = pd.read_csv(path, skipinitialspace=True).copy()
        df.columns = [str(col).strip() for col in df.columns]
        df[TRANSLATION_COL] = label
        return df

    def profile(self):
        return pd.concat(
            [
                self._read_profile(self.csv_a, self.label_a),
                self._read_profile(self.csv_b, self.label_b),
            ],
            ignore_index=True,
        )

    def chapters(self):
        return sorted(self.profile()[CHAPTER_COL].unique(), key=_chapter_number)

    def punctuation_long(self):
        df = self.profile()
        cols = [c for c in df.columns if c.startswith("Punctuation_Rate_")]
        long = df.melt(
            id_vars=[CHAPTER_COL, TRANSLATION_COL],
            value_vars=cols,
            var_name="Punctuation",
            value_name="Rate",
        )
        long["Punctuation"] = long["Punctuation"].str.replace("Punctuation_Rate_", "")
        return long

    def function_words_long(self):
        """Reshape function-word frequency columns into long form with two rankings.

        The profile CSV stores each function word's relative frequency
        (occurrences / total words) in its own ``Function_Word_Freq_<word>``
        column. This method melts those columns into one row per (chapter,
        translation, word) and attaches two ranks:

        - ``Rank`` — per-translation rank: each word's mean relative frequency,
          averaged over that translation's nine chapters, ranked descending
          (rank 1 = most frequent). Used by the "Separate charts" view.
        - ``Global_Rank`` — overall rank across both translations and all
          chapters (rank 1 = most frequent overall). Used by the "Compare in
          one chart" view.

        The dashboard's default "top 5" is simply the five words with the
        lowest rank (1-5) for whichever ranking the active view uses.
        """
        df = self.profile()
        cols = [c for c in df.columns if c.startswith("Function_Word_Freq_")]
        long = df.melt(
            id_vars=[CHAPTER_COL, TRANSLATION_COL],
            value_vars=cols,
            var_name="Function_Word",
            value_name="Frequency",
        )
        long["Function_Word"] = long["Function_Word"].str.replace("Function_Word_Freq_", "")
        trans = (
            long.groupby([TRANSLATION_COL, "Function_Word"])["Frequency"]
            .mean()
            .reset_index(name="Mean")
        )
        trans["Rank"] = (
            trans.groupby(TRANSLATION_COL)["Mean"]
            .rank(method="first", ascending=False)
            .astype(int)
        )
        global_ranks = (
            long.groupby("Function_Word")["Frequency"].mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        global_ranks["Global_Rank"] = range(1, len(global_ranks) + 1)
        long = long.merge(
            trans[[TRANSLATION_COL, "Function_Word", "Rank"]],
            on=[TRANSLATION_COL, "Function_Word"],
        )
        return long.merge(global_ranks[["Function_Word", "Global_Rank"]], on="Function_Word")


def _chapter_number(label):
    return int(str(label).replace(CHAPTER_COL, "").strip())


class ChartBuilder:
    """Builds reusable Altair charts for each feature type."""

    def grouped_bar(self, data, metric, title):
        return (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X(f"{CHAPTER_COL}:N", title="Chapter"),
                xOffset=f"{TRANSLATION_COL}:N",
                y=alt.Y(f"{metric}:Q", title=title),
                color=alt.Color(f"{TRANSLATION_COL}:N", title="Translation"),
            )
            .properties(title=title)
        )

    def line(self, data, title):
        return (
            alt.Chart(data)
            .mark_line(point=True)
            .encode(
                x=alt.X(f"{CHAPTER_COL}:N", title="Chapter"),
                y=alt.Y("Average_Sentence_Length:Q", title=title),
                color=alt.Color(f"{TRANSLATION_COL}:N", title="Translation"),
            )
            .properties(title=title)
        )

    def stacked(self, data, category, value, title, normalize):
        stack = "normalize" if normalize else "zero"
        return (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X(f"{CHAPTER_COL}:N", title="Chapter"),
                xOffset=f"{TRANSLATION_COL}:N",
                y=alt.Y(f"{value}:Q", title=title, stack=stack),
                color=alt.Color(f"{category}:N", title=category.replace("_", " ")),
            )
            .properties(title=title)
        )


class Dashboard:
    '''Renders the interactive Streamlit dashboard.'''

    def __init__(self, data, charts):
        self.data = data
        self.charts = charts

    def run(self):
        st.set_page_config(page_title='Two Faces of Demian', layout='wide')
        st.title('Two Faces of Demian')
        st.caption('Stylometric comparison of two English translations of Demian.')
        self._render_grouped_charts()
        self._render_line()
        self._render_punctuation()
        self._render_function_words()

    def _chapters(self, title):
        options = self.data.chapters()
        return st.multiselect(f'Chapters ({title})', options, default=options)

    def _render_grouped_charts(self):
        st.header('Vocabulary & Structure')
        for metric, title in [
            ('Type_Token_Ratio', 'Type-Token Ratio'),
            ('Paragraph_to_Sentence_Ratio', 'Paragraph-to-Sentence Ratio'),
        ]:
            chapters = self._chapters(title)
            data = self._filter(self.data.profile(), chapters)
            st.altair_chart(
                self.charts.grouped_bar(data, metric, title),
                width='stretch',
            )

    def _render_line(self):
        st.header('Pacing')
        chapters = self._chapters('Average Sentence Length')
        data = self._filter(self.data.profile(), chapters)
        st.altair_chart(
            self.charts.line(data, 'Average Sentence Length'),
            width='stretch',
        )

    def _render_punctuation(self):
        st.header('Punctuation Frequencies')
        chapters = self._chapters('Punctuation Frequencies')
        long = self.data.punctuation_long()
        marks = sorted(long['Punctuation'].unique())
        selected = st.multiselect('Punctuation marks', marks, default=marks)
        normalize = st.checkbox('Normalize punctuation to 100%', value=True)
        data = self._filter(long[long['Punctuation'].isin(selected)], chapters)
        st.altair_chart(
            self.charts.stacked(data, 'Punctuation', 'Rate', 'Punctuation Frequencies', normalize),
            width='stretch',
        )

    def _render_function_words(self):
        st.header('Function Word Distribution')
        long = self.data.function_words_long()
        layout = st.radio('View', ['Compare in one chart', 'Separate charts'], horizontal=True)
        if layout == 'Compare in one chart':
            self._render_combined_function_words(long)
        else:
            for translation in sorted(long[TRANSLATION_COL].unique()):
                self._render_one_function_word_chart(long, translation)

    def _render_combined_function_words(self, long):
        chapters = self._chapters('Function words (comparison)')
        rank_map = self._rank_map(long, 'Global_Rank')
        options = [f'#{rank} {word}' for rank, word in rank_map.items()]
        selected = st.multiselect('Function words (by rank)', options, default=options[:5])
        words = {label.split(' ', 1)[1] for label in selected}
        normalize = st.checkbox('Normalize function words to 100%', value=True)
        data = self._filter(long[long['Function_Word'].isin(words)], chapters)
        st.altair_chart(
            self.charts.stacked(data, 'Function_Word', 'Frequency',
                                'Function Word Distribution (comparison)', normalize),
            width='stretch',
        )

    def _render_one_function_word_chart(self, long, translation):
        sub = long[long[TRANSLATION_COL] == translation]
        chapters = self._chapters(f'Function words ({translation})')
        rank_map = self._rank_map(sub)
        options = [f'#{rank} {word}' for rank, word in rank_map.items()]
        selected = st.multiselect(f'Function words by rank ({translation})', options, default=options[:5])
        words = {label.split(' ', 1)[1] for label in selected}
        normalize = st.checkbox(f'Normalize function words ({translation})', value=True)
        data = self._filter(sub[sub['Function_Word'].isin(words)], chapters)
        st.altair_chart(
            self.charts.stacked(data, 'Function_Word', 'Frequency',
                                f'Function Word Distribution ({translation})', normalize),
            width='stretch',
        )

    @staticmethod
    def _filter(data, chapters):
        return data[data[CHAPTER_COL].isin(chapters)]

    @staticmethod
    def _rank_map(long, rank_col='Rank'):
        ranked = long[['Function_Word', rank_col]].drop_duplicates().sort_values(rank_col)
        return {int(getattr(row, rank_col)): row.Function_Word for row in ranked.itertuples()}


def build_dashboard():
    return Dashboard(TranslationData(CSV_A, CSV_B), ChartBuilder())


if __name__ == "__main__":
    build_dashboard().run()

import streamlit as st
from streamlit_gsheets import GSheetsConnection


def load_css(file_name: str) -> None:
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Config
st.set_page_config(page_title="Data Analyst RNCP Flashcards")
st.title("Questions pour le RNCP Data Analyst")
load_css("style.css")


# Get data from the Google Spreadsheet
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl="10m")

# Category selection
with st.sidebar:
    categories = df["Category"].unique()
    text = "Sélectionnez une ou plusieurs catégories"
    categories_selected = st.multiselect(
        label=text, placeholder=text, options=categories, default=categories
    )

# Initialize session states
if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.answer = None
    st.session_state.shown_answer = False

if categories_selected:
    df_selection = df[df["Category"].isin(categories_selected)]
    if not df_selection.empty:
        selection = df_selection.sample(n=1).iloc[0]
        if st.session_state.question is None or st.session_state.shown_answer:
            st.session_state.question = selection["Question"]
            st.session_state.answer = selection["Answer"]
            st.session_state.shown_answer = False

        st.markdown(
            f'<div class="question">{st.session_state.question}</div>',
            unsafe_allow_html=True,
        )

        button_clicked = st.button("Voir la réponse", key="show_answer")
        if button_clicked:
            st.session_state.shown_answer = True
            st.markdown(
                f'<div class="answer">{st.session_state.answer}</div>',
                unsafe_allow_html=True,
            )

        if st.session_state.shown_answer:
            if st.button("Question suivante :arrow_forward:", key="next_question"):
                st.session_state.shown_answer = False
                st.experimental_rerun()
    else:
        st.markdown(
            '<div class="error">Il n\'y a pas de questions disponibles pour ces catégories.</div>',
            unsafe_allow_html=True,
        )

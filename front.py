import streamlit as st
from htmlTemplates import css, bot_template, user_template

def main():
    st.set_page_config(page_title="Your own AI chat",
                       page_icon="👋")

    st.write(css, unsafe_allow_html=True)


if __name__ == '__main__':
    main()

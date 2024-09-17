import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="ABRomics demo - Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

with st.sidebar:
    st.title('ABRomics KG demo')

st.info('Do not forget to check the documentation of the project !')

st.title('Welcome to the ABRomics Knowledge graph demo !')

st.markdown('')

st.markdown('''The ABRomics KG demo will help you understand how to use a knowledge graph. In this demo you will learn
               how the graph is structured, how to navigate in the graph to retrieve found data and a small introduction
               on SPARQL queries.
             ''')

st.markdown('''The demonstration is intended for all public, researchers and clinicians are welcomed. Further documentation
            about the technical details of the project can be found in the complete documentation
           ''')


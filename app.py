import os
from PIL import Image
import yfinance as yf
import pandas as pd
from pathlib import Path
import streamlit as st
from utils import utils
from dotenv import load_dotenv; load_dotenv()
from lyzr import DataConnector, DataAnalyzr



# Setup your config
st.set_page_config(
    page_title="Expense Tracker",
    layout="centered",  # or "wide" 
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Expense Tracker by Lyzr")
st.markdown("### Welcome to the Expense Tracker!")
st.markdown("Expense Tracker app empowers you to take control of your finances. Seamlessly track your daily expenses, categorize them effortlessly, and gain powerful insights through DataAnalyzr's AI-powered Agent by Lyzr.")

# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Expene Tracker Application

# create directory if it doesn't exist
data = "data"
plot = 'plot'
os.makedirs(data, exist_ok=True)
os.makedirs(plot, exist_ok=True)








def file_checker():
    file = []
    for filename in os.listdir(data):
        file_path = os.path.join(data, filename)
        file.append(file_path)

    return file

       

if __name__ == "__main__":
    style_app()
    select_compnay()
    file = file_checker()
    if len(file)>0:
        analyzr = market_analyzr()
        description, analysis = generating_insights(analyzr)
        if description is not None:
            st.subheader("Description the Company data")
            st.write(description)
            plot_files = os.listdir("./plot")
            st.subheader("Technical Indicators about the company stock")
            for plot_file in plot_files:
                st.image(f"./plot/{plot_file}")
            st.subheader("Recommended Analysis")
            st.write(analysis)
        else:
            st.error('Error: occurs while generating description')

    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr DataAnalyzr agent to generate analysis on data. With DataAnalyzr, you can streamline the complexity of data analytics into a powerful, intuitive, and conversational interface that lets you command data with ease. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)

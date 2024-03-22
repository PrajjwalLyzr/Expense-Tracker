import os
from PIL import Image
import pandas as pd
from pathlib import Path
import streamlit as st
from utils import utils
from datetime import datetime
from dotenv import load_dotenv; load_dotenv()
from lyzr import DataAnalyzr, DataConnector



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

# replace this with your openai api key or create an environment variable for storing the key.
API_KEY = os.getenv('OPENAI_API_KEY')

# create directory if it doesn't exist
data = "data"
plot = 'plot'
os.makedirs(data, exist_ok=True)
os.makedirs(plot, exist_ok=True)


def data_uploader():
    st.subheader("Upload CSV file for analysis")
    # Upload csv file
    uploaded_file = st.file_uploader("Choose csv file", type=["csv"])
    if uploaded_file is not None:
        utils.save_uploaded_file(uploaded_file)
    else:
        utils.remove_existing_files(data)
        utils.remove_existing_files(plot)



def expense_tracker(filepath):
    dataframe = DataConnector().fetch_dataframe_from_csv(file_path=Path(filepath))
    analyzr = DataAnalyzr(df=dataframe, api_key=API_KEY)
    return analyzr



def file_checker():
    file = []
    for filename in os.listdir(data):
        file_path = os.path.join(data, filename)
        file.append(file_path)

    return file

       

if __name__ == "__main__":
    style_app()
    st.markdown("#### Make sure your data in this format")
    utils.data_format()
    data_uploader()
    file = file_checker()
    if len(file)>0:
        month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        selected_month = st.selectbox('Select a Month', month_names)
        current_year = datetime.now().year
        selected_year = st.selectbox("Select a Year:", range(current_year - 30, current_year + 30), index=10)
        if st.button('Submit'):
            path = utils.get_files_in_directory(data)
            analyzr_agent = expense_tracker(filepath=path[0])
            if analyzr_agent is not None:
                insights = utils.generating_insights(analyzr=analyzr_agent, month=selected_month, year=selected_year)
                if insights is not None:
                    plot_files = os.listdir("./plot")
                    st.subheader(f"Expence Insights for {selected_month} {selected_year}")
                    for plot_file in plot_files:
                        st.image(f"./plot/{plot_file}") 
                    st.subheader("Recommended Analysis")
                    utils.show_results(result=insights)

    else:
        st.warning('Please Upload a csv file')

    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr DataAnalyzr agent to generate analysis on data. With DataAnalyzr, you can streamline the complexity of data analytics into a powerful, intuitive, and conversational interface that lets you command data with ease. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)

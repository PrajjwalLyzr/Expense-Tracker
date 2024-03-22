import os
import shutil
import streamlit as st
from pathlib import Path
import pandas as pd

def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")


def get_files_in_directory(directory):
    # This function help us to get the file path along with filename.
    files_list = []

    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list

def save_uploaded_file(uploaded_file):
    # Function to save uploaded file
    remove_existing_files('data')

    file_path = os.path.join('data', uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.read())
    st.success("File uploaded successfully")


def generating_insights(analyzr):
    description = analyzr.dataset_description()
    analysis = analyzr.analysis_recommendation()
    prompts = ["Create a candlestick chart to visualize the open, high, low, and close prices of the stock for each trading day over a specific period",
               "Plot Bollinger Bands around the closing price chart to visualize volatility and potential reversal points",
               "Plot the RSI indicator to assess the stock's momentum and overbought/oversold conditions. RSI values above 70 indicate overbought conditions, while values below 30 indicate oversold conditions",
               "Plot the MACD indicator to identify trend changes and potential buy/sell signals. MACD consists of a fast line (MACD line), slow line (signal line), and a histogram representing the difference between the two lines",
               "Plot a histogram of daily returns (percentage change in closing price) to visualize the distribution of returns and assess risk",
               "Plot a chart showing the high, low, and closing prices for each trading day over a specific period. This provides a comprehensive view of daily price fluctuations.",
               "Overlay moving average lines (e.g.,44-day moving averages) on the closing price chart to smooth out price fluctuations and identify long-term trends."
                ]
    
    utils.remove_existing_files(plot)
    for prompt in prompts:
        vis = analyzr.visualizations(user_input=prompt, dir_path=Path('./plot'))

    return description, analysis


def data_format():
    pass




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


def generating_insights(analyzr, month, year):
    result = {}
    prompts = [f"Create a bar chart showing the total spending for each expense category in {month} {year}. Order the categories by the amount spent from highest to lowest",
               f"Generate a line chart depicting my daily spending throughout {month} {year}. Include the date on the x-axis and the spending amount on the y-axis. Highlight the days with the highest and lowest spending.",
               f"Create a pie chart illustrating the distribution of my spending across the top 3 expense categories in {month} {year}. Label each slice with the category name and the percentage of total spending it represents.",
                ]
    
    remove_existing_files('plot')
    for prompt in prompts:
         result = analyzr.ask(
                                prompt,
                                outputs = ["visualisation"],
                                plot_path = Path('./plot')
                        )

    queries = [
                "What is my total spending this month?",
                "In which category do I spend the most?",
                "How has my spending on groceries changed over the past 3 months?",
    ]

    for query in queries:
        analysis = analyzr.ask(
                                    user_input = query,
                                    outputs = ["insights"]
                            )
        result[query] = analysis['insights']


    return result


def data_format():
    data = {
    'Date': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Amount': [100.00, 50.25, 75.50],
    'Category': ['Groceries', 'Utilities', 'Dining'],
    'Payee': ['Walmart', 'Electricity Company', 'Restaurant'],
    'Description': ['Weekly grocery shopping', 'Electricity bill', 'Dinner with friends']
    }

    sampledf = pd.DataFrame(data)

    # Display DataFrame
    st.write(sampledf)


def show_results(result: dict):
    for query, insight in result.items():
        st.subheader(query)
        st.write(insight)
        st.markdown("---")




# DoppelgangerGPT

This GitHub repository uses OpenAI API, vector search, and langchain to create a personalized digital doppelganger that mimics your language and communication style. Doppelganger provides an AI-based chatbot experience that reflects the user's personality based on KakaoTalk chat data.

## Installation

To get started, run the following command in your terminal:

## Copy code

`pip install -r requirements.txt`
This will install all the required packages for the project.

## Environment Variables

Create a .env file in the root directory and add the following line to set up your OpenAI API key:

`OPENAI_API_KEY="OPENAI_API_KEY"`
Replace OPENAI_API_KEY with your actual API key.

## Dataset

Export your KakaoTalk chat data and place it in data/kakaotalk_data/ with the filename KakaoTalkChats.txt.

## Running the Project

Follow these steps to run the project:

1. Navigate to the data/kakaotalk_data directory in your terminal:

`cd data/kakaotalk_data`

2. Run the following command to generate a /db folder in the root directory:

`python process_data.py`

3. Return to the root directory and run the following command to launch the program:

`python main.py`

We hope you enjoy using DoppelgangerGPT!

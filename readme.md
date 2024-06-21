# GitHub Repository Chat App

## Overview

The GitHub Repository Chat App is an interactive Streamlit application that allows users to chat with GitHub repositories using natural language. Powered by Llama3 and Ollama, this app provides an intuitive interface for querying and exploring GitHub repositories, making it easier to understand codebases and find information quickly.

## Features

- Load and interact with multiple GitHub repositories
- Chat-based interface for asking questions about repositories
- Utilizes Llama 3 for natural language processing
- Efficient embedding and retrieval using ChromaDB
- User-friendly Streamlit interface

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- Ollama installed and running with the Llama3 model
- A GitHub Personal Access Token

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/h9-tect/Chat_With_Github.git
   cd Chat_With_Github
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your GitHub token:
   - For local development, you can set it as an environment variable:
     ```
     export GITHUB_TOKEN=your_github_token_here
     ```
   - For Streamlit Cloud deployment, add it to your app's secrets.

## Usage

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter a GitHub repository in the format `username/repo` in the input field.

4. Once the repository is loaded, you can start asking questions about it in the chat interface.

5. The app will provide answers based on the content of the loaded repositories.

## Configuration

You can modify the following parameters in the `create_embedchain_bot` function to adjust the behavior of the language model:

- `max_tokens`: Maximum number of tokens in the generated response
- `temperature`: Controls the randomness of the output (0.0 to 1.0)


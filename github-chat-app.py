import tempfile
import os
import streamlit as st
from embedchain import App
from embedchain.loaders.github import GithubLoader

# Use st.secrets for sensitive information
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", os.getenv("GITHUB_TOKEN"))

def get_loader():
    if not GITHUB_TOKEN:
        st.error("GitHub token is missing. Please set it in your Streamlit secrets or environment variables.")
        st.stop()
    return GithubLoader(config={"token": GITHUB_TOKEN})

@st.cache_resource
def create_embedchain_bot():
    db_path = tempfile.mkdtemp(suffix="chroma")
    st.info(f"Created Chroma DB at {db_path}")
    return App.from_config(
        config={
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": "llama3:instruct",
                    "max_tokens": 250,
                    "temperature": 0.5,
                    "stream": True,
                    "base_url": 'http://localhost:11434'
                }
            },
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {
                "provider": "ollama",
                "config": {
                    "model": "llama2:13b",
                    "base_url": 'http://localhost:11434'
                }
            },
        }
    )

def load_repo(app, git_repo):
    try:
        with st.spinner(f"Loading {git_repo} into knowledge base..."):
            app.add(f"repo:{git_repo} type:repo", data_type="github", loader=st.session_state.loader)
        st.success(f"Added {git_repo} to knowledge base!")
    except Exception as e:
        st.error(f"Error loading repository: {str(e)}")

def main():
    st.set_page_config(page_title="GitHub Repo Chat", page_icon="💬", layout="wide")
    
    st.title("Chat with GitHub Repository 💬")
    st.caption("This app allows you to chat with a GitHub Repo using Llama 2 running with Ollama")

    if "loader" not in st.session_state:
        st.session_state.loader = get_loader()

    if "app" not in st.session_state:
        st.session_state.app = create_embedchain_bot()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "loaded_repos" not in st.session_state:
        st.session_state.loaded_repos = set()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Chat")
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.chat_history:
                st.write(message)

        prompt = st.text_input("Ask any question about the GitHub Repo", key="prompt_input")

        if prompt:
            with st.spinner("Generating response..."):
                answer = st.session_state.app.chat(prompt)
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.experimental_rerun()

        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.experimental_rerun()

    with col2:
        st.subheader("Repository Management")
        git_repo = st.text_input("Enter the GitHub Repo (format: username/repo)", key="repo_input")

        if git_repo and git_repo not in st.session_state.loaded_repos:
            load_repo(st.session_state.app, git_repo)
            st.session_state.loaded_repos.add(git_repo)

        st.subheader("Loaded Repositories")
        for repo in st.session_state.loaded_repos:
            st.write(f"- {repo}")

if __name__ == "__main__":
    main()

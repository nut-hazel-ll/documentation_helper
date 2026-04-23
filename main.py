from typing import Set
from backend.core import run_llm
import streamlit as st

# Set page config with LangChain-inspired theme
st.set_page_config(
    page_title="Python Documentation Helper",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for LangChain-inspired theme
st.markdown("""
    <style>
    /* Main theme colors - LangChain green */
    :root {
        --langchain-green: #10B981;
        --langchain-green-dark: #059669;
        --langchain-green-light: #D1FAE5;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --bg-primary: #FFFFFF;
        --bg-secondary: #F9FAFB;
        --border-color: #E5E7EB;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    h1 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: var(--bg-secondary) !important;
    }
    
    /* Button styling - green accent */
    .stButton > button {
        background-color: var(--langchain-green) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: var(--langchain-green-dark) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2) !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border: 1px solid var(--border-color) !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--langchain-green) !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem !important;
        border-radius: 0.75rem !important;
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stChatMessage"] {
        background-color: var(--bg-secondary) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    /* Markdown links */
    a {
        color: var(--langchain-green) !important;
        text-decoration: none !important;
    }
    
    a:hover {
        color: var(--langchain-green-dark) !important;
        text-decoration: underline !important;
    }
    
    /* Divider styling */
    hr {
        border-color: var(--border-color) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: var(--langchain-green-light) !important;
        border-left: 4px solid var(--langchain-green) !important;
        color: var(--langchain-green-dark) !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: var(--langchain-green) !important;
        border-top-color: transparent !important;
    }
    
    /* Sidebar markdown styling */
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    /* Profile section styling */
    [data-testid="stSidebar"] img {
        border-radius: 0.5rem !important;
        border: 2px solid var(--langchain-green-light) !important;
    }
    
    /* Chat input area */
    .stTextInput label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    /* Code blocks */
    code {
        background-color: var(--bg-secondary) !important;
        color: var(--langchain-green-dark) !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 0.25rem !important;
    }
    
    /* Custom header accent */
    .main h1::before {
        content: "🔗";
        margin-right: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize user information in session state
if "user_info" not in st.session_state:
    st.session_state["user_info"] = {
        "name": "Luca Zhang",
        "email": "luca.zhang@example.com",
        "profile_picture_url": "https://ui-avatars.com/api/?name=Luca+Zhang&background=random&size=128"
    }

# Sidebar with user information
with st.sidebar:
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="color: #1F2937; font-weight: 600; font-size: 1.5rem; margin-bottom: 0.5rem;">
                👤 User Profile
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Profile picture
    profile_pic_url = st.session_state["user_info"]["profile_picture_url"]
    st.image(profile_pic_url, width=150, caption="Profile Picture")
    
    st.markdown("---")
    
    # User name
    st.markdown(f"**Name:** {st.session_state['user_info']['name']}")
    
    # User email
    st.markdown(f"**Email:** {st.session_state['user_info']['email']}")
    
    st.markdown("---")
    
    # Edit user information
    with st.expander("Edit Profile"):
        new_name = st.text_input("Name", value=st.session_state["user_info"]["name"])
        new_email = st.text_input("Email", value=st.session_state["user_info"]["email"])
        new_profile_url = st.text_input(
            "Profile Picture URL", 
            value=st.session_state["user_info"]["profile_picture_url"],
            help="Enter a URL to an image or use a service like ui-avatars.com"
        )
        
        if st.button("Update Profile"):
            st.session_state["user_info"]["name"] = new_name
            st.session_state["user_info"]["email"] = new_email
            st.session_state["user_info"]["profile_picture_url"] = new_profile_url
            st.success("Profile updated!")
            st.rerun()

# Main title with LangChain-inspired styling
st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #1F2937; font-weight: 700; font-size: 2.5rem; margin-bottom: 0.5rem;">
            Python Documentation Helper
        </h1>
        <p style="color: #6B7280; font-size: 1.1rem; margin-top: 0;">
            Ask questions about your documentation and get instant answers powered by AI.
        </p>
    </div>
""", unsafe_allow_html=True)

prompt = st.text_input("", placeholder="Enter your prompt here...", label_visibility="collapsed")

if ("user_prompt_history" not in st.session_state
    and "chat_answers_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_answers_history"] = []
    st.session_state["chat_history"] = []

def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"- {source}\n"
    return sources_string


if prompt:
    with st.spinner("Generating response.."):
        generated_response = run_llm(query=prompt, chat_history=st.session_state["chat_history"])
        sources = set(
            [doc.metadata["source"] for doc in generated_response["context"]]
        )

        formatted_response = (
            f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai",generated_response["answer"]))

# Chat history display with LangChain-inspired styling
if st.session_state["chat_answers_history"]:
    st.markdown("---")
    st.markdown("""
        <div style="margin-top: 2rem;">
            <h2 style="color: #1F2937; font-weight: 600; font-size: 1.5rem; margin-bottom: 1rem;">
                Chat History
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        with st.chat_message("user"):
            st.write(user_query)
        with st.chat_message("assistant"):
            st.markdown(generated_response)

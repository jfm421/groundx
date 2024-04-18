import streamlit as st
import groundx-python-sdk as groundx
import openai

# Initialize GroundX and OpenAI clients using Streamlit secrets
groundx_client = groundx.Groundx(api_key=st.secrets["groundx_api_key"])
openai.api_key = st.secrets["openai_api_key"]

def search_groundx(query):
    """Function to perform a search on GroundX and return text results."""
    try:
        content_response = groundx_client.search.content(query=query)
        results = content_response.body["search"]
        return results["text"]
    except Exception as e:
        return f"An error occurred: {str(e)}"

def generate_response(text):
    """Function to send text to OpenAI's ChatGPT and receive a response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify your model version here
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer the question based on the content provided."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.title('Integrating GroundX and OpenAI for Enhanced Conversations')

user_query = st.text_input('Enter your query to search on GroundX:')
if st.button('Search and Generate Response'):
    if user_query:
        search_results = search_groundx(user_query)
        st.text_area("Search Results", search_results, height=300)

        response = generate_response(search_results)
        st.text_area("Generated Response from ChatGPT", response, height=150)
    else:
        st.error("Please enter a query to proceed.")

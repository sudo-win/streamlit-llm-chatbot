import chromadb
import streamlit as st
from PyPDF2 import PdfReader
import ollama

client = chromadb.PersistentClient(
    path="<any-folder-path>")

collection_name = 'my-pdf'
pdf_collection = client.get_or_create_collection(collection_name)
base_path = "<pdf-file-folder-path>"


def extract_data(path: str):
    print('uploading data chroma db')

    client.delete_collection(collection_name)
    pdf_collection = client.create_collection(collection_name)

    reader = PdfReader(path)
    number_of_pages = len(reader.pages)
    for page_number in range(0, number_of_pages):
        data = []
        page = reader.pages[page_number]
        text = page.extract_text()
        data.append(text)
        pdf_collection.add(documents=data,
                           ids=[str(page_number)]
                           )

    print(f'PDF data added to Chroma collection from {str(path)} ')


# Define a simple function for chatbot responses

def chatbot_response(user_input):
    print('querying chroma db')

    query = user_input
    results = pdf_collection.query(
        query_texts=[query],
        n_results=20
    )

    print('received documents from chromadb')

    retrieved_docs = results['documents'][0]  # The documents retrieved from Chroma

    # print(retrieved_docs)
    prompt = "Based on the following documents, answer the question:\n\n"
    prompt += "\n".join(retrieved_docs)
    prompt += f"\n\nQuestion: {query}\nAnswer:"

    response = ollama.chat(model="gemma3:1b", messages=[{"role": "user", "content": prompt}])

    return response.message


uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")

if uploaded_file is not None:
    str_path = base_path + str(uploaded_file.name)
    extract_data(str_path)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    print('received prompt')
    response = chatbot_response(prompt)
    print('got prompt')

    # response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

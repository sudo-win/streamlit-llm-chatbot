# streamlit-llm-chatbot
This app leverages Streamlit for the user interface and Chroma DB for efficient document storage and retrieval. It allows you to upload a PDF, convert its content into a searchable database, and interact with it as a chatbot.

Steps to run:
1) Update the Chroma DB and base pdf location path in the code.
2) Download [ollama application](https://ollama.com/download/windows) and make sure it is running in the background.
3) Run</br>
git clone https://github.com/sudo-win/streamlit-llm-chatbot.git</br>
cd streamlit-llm-chatbot</br>
pip install -r requirements.txt
4) Run</br>
streamlit run app.py 

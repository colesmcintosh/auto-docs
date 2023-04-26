import streamlit as st
import openai
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()
# Replace with your OpenAI API key
priv_key=os.getenv("PRIV_KEY")
openai.api_key = priv_key

def chunk_code(code: str, chunk_size: int = 8000) -> List[str]:
    return [code[i:i + chunk_size] for i in range(0, len(code), chunk_size)]

def generate_documentation(prompt: str, doc_type: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
    {
        "role": "system",
        "content": "You are a helpful assistant specialized in analyzing and explaining code. Provide a detailed and clear explanation of the given code, covering its functionality, logic, and any important concepts involved.",
    },
    {
        "role": "user",
        "content": f"Generate a {doc_type} for the following code:\n{prompt}\n",
    },
])
    return response.choices[0].message['content'].strip()

def main():
    st.set_page_config(page_title="Auto Docs", page_icon="📄", layout="centered")
    st.title("Auto Docs 📄")
    st.write("Upload a code file and generate documentation using GPT-4.")
    
    file = st.file_uploader("Select file", type=["py", "js", "java", "cpp", "c", "rb", "php", "html", "css"])
    doc_type = st.text_input("What kind of document do you need?")

    if st.button("Generate Documentation"):
        if file:
            with st.spinner("Generating documentation..."):
                code = file.read().decode()
                chunks = chunk_code(code)
                for i, chunk in enumerate(chunks, 1):
                    documentation = generate_documentation(chunk, doc_type)
                    st.write(f"Documentation for file {file.name} (part {i}):")
                    st.write(documentation)

if __name__ == "__main__":
    main()

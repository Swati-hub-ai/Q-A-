import streamlit as st
import os
import groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



from dotenv import load_dotenv

load_dotenv()

#langsmith tracking 
os.environ['Langchain_api']=os.getenv('Langchain_api')
os.environ['LANGCHAIN_TRACING_V2']="True"
os.environ['LANGCHAIN_PROJECT']="Q&A Chatbot Using GROQ"

#prompt template
prompt=ChatPromptTemplate.from_messages(
    (
        ("system","You are a Helpful assistant. Please response to the user queries."),
        ("user","Question:{question}")
    )
)

def generate_response(question,api_key,engine,temperature,max_tokens):
    llm = ChatGroq(model_name=engine, groq_api_key=api_key)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer


#Title of the app 
st.title("Enhanced Q&A Chatbot with GROQ")

#SIdebar for setting
st.sidebar.title("Setting")
api_key=st.sidebar.text_input("Enter your Groq Api Key:", type="password")

#Select down to select various Groq model
engine=st.sidebar.selectbox("Select Groq LLm Model", ["llama3-8b-8192", "gemma2-9b-it", "mistral-saba-24b"])

#Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50, max_value=300, value=150)

#main interface for  user input
st.write("Go ahead and ask any question")
user_input=st.text_input("You:")

if user_input:
    response=generate_response(user_input,api_key,engine,temperature,max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter the OPen AI aPi Key in the sider bar")
else:
    st.write("Please provide the user input")




 #Option to clear chat history
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()
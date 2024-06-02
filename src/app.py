import sqlite3
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sqlite3
from main import BlogPostCreator
import streamlit as st
import os


with st.sidebar:
    "## ✍️ Blog Post Generator"
            
    web_references = st.number_input(
        label="Enter number of web references to use",
        max_value=10,
        min_value=1,
        value=3,
    )
    
    openai_api_key = st.text_input(
        label="OpenAI API Key",
        type="password"
        )
    
    "You can get your OpenAI API key from [here](https://platform.openai.com/api-keys)"
        
    "[View the source code](https://github.com/jordan-jakisa/blog_post_writer)"
    
    
    os.environ['OPENAI_API_KEY'] = openai_api_key


st.title(" ✍️ Blog Post Generator ")

with st.form(key="generate_blog_post"):
    keyword = st.text_input(label= "Enter a keyword", placeholder="")

    submitted = st.form_submit_button("Generate blog post")
    
    if submitted  and not openai_api_key:
        st.info("Please enter your OpenAI API key")
        
    elif submitted and not keyword:
        st.warning("Please enter a keyword")
        
    elif submitted:
        creator = BlogPostCreator(keyword, web_references)       
        response = creator.create_blog_post()
        
        if isinstance(response, Exception):
            print(f"An error occurred: {response}")
            st.info(f"Please try again!")
            st.error(f"An error occurred: {response}")
        else:
            st.write("### Generated blog post")
            st.write(response)
            
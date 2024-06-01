from main import BlogPostCreator
import streamlit as st
import os


with st.sidebar:
    st.markdown(
        """
        ## Blog Post Generator
        This app generates a blog post based on a keyword.
        """
    )
    
    "[View the source code](https://github.com/jordan-jakisa/blog_post_writer)"
    
    openai_api_key = st.text_input(
        label="OpenAI API Key",
        placeholder="Enter your OpenAI API key",
        type="password"
        )
    
    os.environ['OPENAI_API_KEY'] = openai_api_key


st.title(" ✍️ Blog Post Generator ")

keyword = st.text_input(
    label= "Enter a keyword: ",
    placeholder="The impact of AI on content creation"
    )

if keyword and openai_api_key:
    response = BlogPostCreator(keyword=keyword).create_blog_post()
    st.write("### Generated blog post")
    st.write(response)
else :
    st.info("Please enter a keyword and your OpenAI API key")
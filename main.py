import os
import re
import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.environ['OPENAI_API_KEY']
gemini_api_key = os.environ['GEMINI_API_KEY']

llm = OpenAI(api_key=openai_api_key, max_tokens=2000)
#llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

def parse_links(search_results: str):
    print("-----------------------------------")
    print("Parsing links ...")
    return re.findall(r'link:\s*(https?://[^\],\s]+)', search_results)


def generate_blog(keyword, context):
    try:
        print("-----------------------------------")
        print("Generating blog post ...")
        template = """
        Given the following information, generate a blog post
        
        Write a full blog post that will rank for the following keywords: {keyword}
        
        Instructions:
        
        The blog should be properly and beautifully formatted using markdown.
            
        The blog title should be SEO optimized.
        
        Each sub-section should have at least 3 paragraphs.
        
        Each section should have at least three subsections.
        
        Sub-section headings should be clearly marked.
        
        Clearly indicate the title, headings, and sub-headings using markdown.

        Each section should cover the specific aspects as outlined.

        For each section, generate detailed content that aligns with the provided subtopics. Ensure that the content is informative and covers the key points.

        Ensure that the content flows logically from one section to another, maintaining coherence and readability.

        Where applicable, include examples, case studies, or insights that can provide a deeper understanding of the topic.

        Always include discussions on ethical considerations, especially in sections dealing with data privacy, bias, and responsible use.

        In the final section, provide a forward-looking perspective on the topic and a conclusion.
        
        Please ensure proper and standard markdown formatting always.
        
        Context:

        The following information is summaries from blog posts with similar titles, use it to inform your writing style and content.
        
        {context}
        
        """

        prompt = PromptTemplate(template=template, input_variables=["keyword", "context"])
        chain = prompt | llm

        outline_response = chain.invoke({"keyword": keyword, "context": context})

        return outline_response

    except Exception as e:
        print(f"An error occurred while generating the blog post: {e}")
        return None

def save_file(content: str, filename: str):
    print("-----------------------------------")
    print("Saving file...")
    with open(filename, 'w') as f:
        f.write(content)
    print(f" 🥳 File saved as {filename}")

def get_links(keyword):
    try:
        print("-----------------------------------")
        print("Getting links ...")

        wrapper = DuckDuckGoSearchAPIWrapper(max_results=2)
        search = DuckDuckGoSearchResults(api_wrapper=wrapper)
        results = search.run(tool_input=keyword)

        links = []

        for link in parse_links(results):
            links.append(link)
        
        return links
    
    except Exception as e:
        print(f"An error occurred while getting links: {e}")
        return []

def get_text_content(link):
    print("-----------------------------------")
    print(f"Getting page content from {link} ...")
    
    try:
        response = requests.get(link)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        text_components = soup.find_all(['p', 'h1', 'h2', 'h3'])
        
        text = "\n".join([t.get_text() for t in text_components])
        
        print(text)
        
        summarize_page(text)

        return text
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def summarize_page(text):
    try:
        print("-----------------------------------")
        print(f"Summarizing page content ...")

        prompt = PromptTemplate(
            input_variables=["text"],
            template="""
                You are a proficient summarizer tasked with condensing blog posts into concise and neat three-paragraph summaries. Your summaries should preserve the key ideas, structure, and tone of the original post. Here’s what you need to do:

                Read the provided blog post carefully.
                Identify and extract the main ideas and supporting details.
                Condense the information into three coherent paragraphs that retain the essence and flow of the original content.
                Please ensure that the summary is clear, concise, and well-organized, capturing the original post's key points and maintaining its tone.

                Summarize the following: 

                {text}
            """
        )

        chain = prompt | llm
        response = chain.invoke(text)
        print(f"Response: {response}")
        return response

    except Exception as e:
        print(f"An error occurred while summarizing the page content: {e}")
        return ""

def main():
    keyword = "Mobile development"
    context = ""
    
    links = get_links(keyword)
    
    for link in links:
        text = get_text_content(link)
        context += "\n" + text
        
    blog = generate_blog(keyword, context)
    save_file(blog, keyword + ".md")
    print("Success! 🎉")

main()
import re
import os
import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
import requests
from bs4 import BeautifulSoup

openai_api_key = os.environ['OPENAI_API_KEY']

keyword = "INTP personality type"

llm = OpenAI(api_key=openai_api_key, max_tokens=2000)


def parse_links(search_results: str):
    print("-----------------------------------")
    print("Parsing links...")
    return re.findall(r'link:\s*(https?://[^\],\s]+)', search_results)


def get_h2_elements(url: str):
    print("-----------------------------------")
    print("Getting h2 elements...")
    web_response = requests.get(url)
    web_response.raise_for_status()

    soup = BeautifulSoup(web_response.content, 'html.parser')

    h2_elements = soup.findAll('h2')

    h2_texts = [h2.get_text() for h2 in h2_elements]

    return h2_texts


def get_brainstorm_questions(keyword: str, h2_elements: str):
    print("-----------------------------------")
    print("Generating brainstorm questions...")

    keyword = keyword
    h2_elements = h2_elements

    template = """
        
        {question}
    
        Generate 10 questions to write an SEO optimized blog post on this !keyword 

        Similar top performing blog posts have the following h2 elements: !h2_elements
        
        Return 10 answers in a numbered format and keep them brief and relevant to the topics  
              
    """

    template = template.replace("!keyword", keyword).replace("!h2_elements", h2_elements)

    prompt = PromptTemplate.from_template(template)

    chain = prompt | llm

    question_response = chain.invoke("")

    return question_response

def generate_blog(keyword=keyword):
    print("-----------------------------------")
    print("Generating blog outline...")
    template = """
    {question}
    
    Write a full blog post that will rank for the following keywords: !keyword
    
        
    Instructions:
    
    The blog should be in properly and beautifully formatted using markdown.
        
    The blog title should be SEO optimized.
    
    Each sub-section should have least 3 paragraphs.
    
    Each section should have at least three subsection.
    
    Sub-section headings should be clearly marked.
    
    Clearly indicate the title, headings and sub-headings using markdown.

    Each section should cover the specific aspects as outlined.

    For each section, generate detailed content that aligns with the provided subtopics. Ensure that the content is informative and covers the key points.

    Ensure that the content flows logically from one section to another, maintaining coherence and readability.

    Where applicable, include examples, case studies, or insights that can provide a deeper understanding of the topic.

    Always include discussions on ethical considerations, especially in sections dealing with data privacy, bias, and responsible use.

    In the final section, provide a forward-looking perspective on the topic and a conclusion.
    
    Please, ensure proper and standard markdown formatting always.
    """

    template = template.replace("!keyword", keyword)

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm

    outline_response = chain.invoke(f"Given the following information, genenrate a blog post")

    return outline_response


def save_file(content: str, filename: str):
    print("-----------------------------------")
    print("Saving file...")
    with open(filename, 'w') as f:
        f.write(content)
    print(f" 🥳 File saved as {filename}")


def get_headings() -> str:
    print("-----------------------------------")
    print("Getting headings...")

    wrapper = DuckDuckGoSearchAPIWrapper(max_results=3)
    search = DuckDuckGoSearchResults(api_wrapper=wrapper)
    results = search.run(tool_input=keyword)

    headings = []

    for link in parse_links(results):
        get_page_text(link)
        headings.append(get_h2_elements(link))

    flat_headings = [item for sublist in headings for item in sublist]

    return ', '.join(flat_headings)


def get_page_text(link):
    print("-----------------------------------")
    print(f"Getting page text for ==> {link}...")
    try:
        response = requests.get(link)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        text_components = soup.find_all(text=True)

        page_text = ' '.join(text_components)

        return page_text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

    

# headings = get_headings()
# questions = get_brainstorm_questions(keyword, headings)
blog_post = generate_blog()

save_file(blog_post, f"{keyword}.md")
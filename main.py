import os
import re
import requests
import bs4
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI, OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
keyword = "AI in education"

def parse_links(search_results: str):
    print("-----------------------------------")
    print("Parsing links ...")
    return re.findall(r'link:\s*(https?://[^\],\s]+)', search_results)


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

# step 1: Load documents
bs4_strainer = bs4.SoupStrainer(('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'))
document_loader = WebBaseLoader(
    web_path=(get_links(keyword=keyword))
)

docs = document_loader.load()

# step 2: text splitting
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)

splits = splitter.split_documents(docs)

# step 3: Indexing and vector storage
vector_store = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# step 4: retrieval
retriever = vector_store.as_retriever(search_type="similarity", search_kwards={"k": 6})

# step 5 : Generation
llm = ChatOpenAI()

template = """
        Given the following information, generate a blog post
        
        Write a full blog post that will rank for the following keywords: {question}
        
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
        
        """

prompt = PromptTemplate.from_template(template=template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    { "context" : retriever | format_docs, "question" : RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
    )

response = chain.invoke(input=keyword)

save_file(response, keyword + ".md")
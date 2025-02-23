import os
import re

import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agents.prompts import BLOG_CREATOR_PROMPT

class BlogPostCreator:
    def __init__(self, keyword, number_of_web_references):
        self.keyword = keyword
        self.number_of_web_references = number_of_web_references
        self.llm = ChatOpenAI(model="gpt-4o")

    def parse_links(self, search_results: str):
        print("-----------------------------------")
        print("Parsing links ...")
        return re.findall(r'link:\s*(https?://[^\],\s]+)', search_results)

    def save_file(self, content: str, filename: str):
        print("-----------------------------------")
        print("Saving file in blogs ...")
        directory = "blogs"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f" 🥳 File saved as {filepath}")

    def get_links(self):
        try:
            print("-----------------------------------")
            print("Getting links ...")

            wrapper = DuckDuckGoSearchAPIWrapper(max_results=self.number_of_web_references)
            search = DuckDuckGoSearchResults(api_wrapper=wrapper)
            results = search.run(tool_input=self.keyword)

            links = []
            for link in self.parse_links(results):
                links.append(link)

            return links

        except Exception as e:
            print(f"An error occurred while getting links: {e}")

    def create_blog_post(self):
        try:
            print("-----------------------------------")
            print("Creating blog post ...")

            # Define self and docs variables
            self = BlogPostCreator(keyword=self.keyword, number_of_web_references=self.number_of_web_references)
            docs = []

            # Define splitter variable
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=400,
                add_start_index=True,
            )

            # Load documents
            bs4_strainer = bs4.SoupStrainer(('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'))

            document_loader = WebBaseLoader(
                web_path=(self.get_links())
            )

            docs = document_loader.load()

            # Split documents
            splits = splitter.split_documents(docs)

            # step 3: Indexing and vector storage
            vector_store = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())

            # step 4: retrieval
            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 10})

            # step 5 : Generation

            prompt = PromptTemplate.from_template(template=BLOG_CREATOR_PROMPT)

            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            chain = (
                    {"context": retriever | format_docs, "keyword": RunnablePassthrough()}
                    | prompt
                    | self.llm
                    | StrOutputParser()
            )

            return chain.invoke(input=self.keyword)

        except Exception as e:
            return e

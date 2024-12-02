<h1 align="center">✍️ Blog Post Generator</h1>

<div id="top" align="center">
  
![GitHub Repo stars](https://img.shields.io/github/stars/jordan-jakisa/blog_post_writer?style=social)
![GitHub forks](https://img.shields.io/github/forks/jordan-jakisa/blog_post_writer?style=social)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/JakisaJordan)](https://twitter.com/JakisaJordan)

</div>

The blog post creator agent is a python script that uses the DuckDuckGo Search API and OpenAI's GPT-3 model to automate the creation of blog posts.

## Demo
https://github.com/jordan-jakisa/blog_post_writer/assets/72340216/ac194af8-789f-4849-83c6-176942119922

Try it [here](https://ai-blog-post-generator.streamlit.app/)


## Features
- Fetches search results from DuckDuckGo based on a given keyword.
- Parses the links from the search results.
- Extracts the text content from each link.
- Generates a blog post based on the given keyword and internet search results as input to the LLM

## How to use
- Visit the web app by clicking this link [https://ai-blog-post-generator.streamlit.app/](https://ai-blog-post-generator.streamlit.app/)
- Enter the number of web references you want to use. (Max 10).
- Enter your [OpenAI API key](https://platform.openai.com/api-keys)
- Enter the keyword you want to generate a blog post for.
- Click on the "Generate blog post" button.

## Architecture
The agent basically consists of the following components

1. **Document loading**: The first step which is most necessary is to perform an internet search, and then load the retrieved texts from the internet into a document using a DocumentLoader. 
2. **Splitting the documents**: The next step is to split the documents into smaller chunks. Splitting documents enables faster searching and also enables us to fit as much relevant data into the context window of the LLM that we are going to use.
3. **Storage**: The split documents have to be stored in a Vector database/Vector store. But before we save the chunks of documents we need to first embed them using OpenAIEmbeddings and then we can store the embeddings into our Vector Store. Embeddings are easily searchable because we can compute similarity scores easily which enables semantic search across the document chunks.

![indexing architecture](https://github.com/jordan-jakisa/blog_post_writer/assets/72340216/c1b4f7cf-d113-4ae1-9371-a12013931cb6)

4. **Retrieval**: When  a user enters keywords to generate a blog post for, we want to be able to get the necessary chunks of data from the Vector store which will be relevant to the keywords. This is enabled through the retriever which helps to extract information from the vector store given the keyword.
5. **Blog generation**: To generate the blog post, we shall pass the retrieved document chunks and the user keyword/keywords as a prompt to the LLM which generates the final blog post.

![generation architecture](https://github.com/jordan-jakisa/blog_post_writer/assets/72340216/ca11afdd-0933-4ee6-9964-162ad4d5a188)

## Installation

1. Clone the repository:
```
git clone https://github.com/jordan-jakisa/blog_post_writer.git
```
2. Navigate to the project directory:
```
cd blog-post-creator
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Enter the following commands to run the app:
```
streamlit run src/app.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

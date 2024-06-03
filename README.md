<h1 align="center">✍️ Blog Post Generator</h1>

<div id="top" align="center">
  
![GitHub Repo stars](https://img.shields.io/github/stars/jordan-jakisa/blog_post_writer?style=social)
![GitHub forks](https://img.shields.io/github/forks/jordan-jakisa/blog_post_writer?style=social)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/JakisaJordan)](https://twitter.com/JakisaJordan)

</div>

The blog post creator agent is a python script that uses the DuckDuckGo Search API and OpenAI's GPT-3 model to automate the creation of blog posts.

![image](https://github.com/jordan-jakisa/blog_post_writer/assets/72340216/a7d701fe-19d8-4d10-8b99-173366ad60b3)


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
The first part of the architecture focuses on collecting the relevant information about a topic, loading the documents, splitting them into easily searchable chunks, embedding the chunks and storing them in a vector store. The purpose of the splitting is to break down the information into small, manageable chunks that can be passed to an LLM without breaking the context boundary, and also to make searching the data and making inferences super fast.

![indexing architecture](https://github.com/jordan-jakisa/blog_post_writer/assets/72340216/c1b4f7cf-d113-4ae1-9371-a12013931cb6)

The second part takes a keyword for the blog from the user, vectorises it and uses it to search our vector store for similar chunks of data that might be useful or relevant to the keyword. We then pass the retrieved information, along with the prompt, to the LLM to generate a blog post in the context of the keyword.

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

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

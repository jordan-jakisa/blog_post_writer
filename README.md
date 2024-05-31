# Blog creator agent

Automated blog post creator is a Python application that uses the DuckDuckGo Search API and OpenAI's GPT-3 model to automate the creation of blog posts.

## Features

- Fetches search results from DuckDuckGo based on a given keyword.
- Parses the links from the search results.
- Extracts the text content from each link.
- Generates a blog post based on the given keyword and internet search results as context
- Saves the generated blog post as a markdown file.

## Architecture

![indexing architecture](https://github.com/jordan-jakisa/blog_post_writer/assets/72340216/c1b4f7cf-d113-4ae1-9371-a12013931cb6)

![generation architecture](https://github.com/jordan-jakisa/blog_post_writer/assets/72340216/ca11afdd-0933-4ee6-9964-162ad4d5a188)

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/blog-post-creator.git
```

2. Navigate to the project directory:

```
cd blog-post-creator

```

3. Install the required dependencies:

```
pip install -r requirements.txt

```


## Usage

1. Set your OpenAI API key as an environment variable in a `.env` file
```
OPENAI_API_KEY=<your_openai_api_key>
```
2. Run the main script with Python:

```
python main.py
```

3. The script will generate a blog post and save it as a markdown file in the `blogs` directory.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Automated Blog Post Creator

Automated Blog Post Creator is a Python application that uses the DuckDuckGo Search API and OpenAI's GPT-3 model to automate the creation of blog posts.

## Features

- Fetches search results from DuckDuckGo based on a given keyword.
- Parses the links from the search results.
- Extracts the text content from each link.
- Uses OpenAI's GPT-3 model to generate a blog post based on the extracted headings.
- Saves the generated blog post as a markdown file.

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

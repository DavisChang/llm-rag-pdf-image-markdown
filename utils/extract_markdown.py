import markdown
from langchain.schema import Document
import re
import markdown
from bs4 import BeautifulSoup


def clean_markdown(markdown_content):
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove specific unwanted elements (e.g., script, style, etc.)
    for tag in soup(["script", "style", "code", "pre"]):
        tag.decompose()

    # Remove images, links, and badges (if needed)
    for tag in soup.find_all(["img", "a"]):
        tag.decompose()

    # Get the cleaned text
    cleaned_text = soup.get_text(separator="\n")

    # Further cleanup to remove multiple newlines and extra spaces
    cleaned_text = re.sub(r"\n+", "\n", cleaned_text).strip()

    return cleaned_text


def parse_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert markdown to HTML (or keep it in markdown, depending on your needs)
    md_original_content = markdown.markdown(md_content)
    # Clean the markdown content
    html_content = clean_markdown(md_original_content)

    # Create a LangChain Document object
    document = Document(page_content=html_content, metadata={"source": file_path})

    return document


def load_documents_from_markdown(folder_path):
    import os

    documents = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".md"):
            file_path = os.path.join(folder_path, file_name)
            document = parse_markdown(file_path)
            documents.append(document)
    return documents


# Example usage
folder_path = "../assets/md/"
documents = load_documents_from_markdown(folder_path)
for doc in documents:
    print(doc.page_content)  # This will print the HTML content of each markdown file

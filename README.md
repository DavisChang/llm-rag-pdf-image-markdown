# LLM RAG 

LLMs RAG + Ollama + LangChain + Chroma + PDF, Image, Markdown + Testing

### LangChain

1. DirectoryLoader (PyPDFDirectoryLoader, UnstructuredPDFLoader)
2. RecursiveCharacterTextSplitter
3. load_evaluator (Embedding distance)
4. Format prompt text
5. Call the LLM model with prompt

#### PyPDFDirectoryLoader
load text-based content from PDF file


#### Improve the quality of yor rag systems
Improving RAG with Better Document Analysis (Markdown)

	•	Problem with regular chunking and processing PDFs
    •	Loss of context
    •	Problems with tables and document structure
    •	Garbage in → Garbage out
	•	Introduction to Azure Document Intelligence (and share alternatives)
    •	https://github.com/tesseract-ocr/tesseract
    •	https://cloud.google.com/document-ai
    •	https://aws.amazon.com/textract/
	•	How to set up Azure Document Intelligence (creating the resource + getting the keys)
    •	Less than €0.01 per page

[Azure Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/use-sdk-rest-api?view=doc-intel-4.0.0&tabs=windows&pivots=programming-language-python)
[Types of chunking](https://www.rungalileo.io/blog/mastering-rag-advanced-chunking-techniques-for-llm-applications)


### Marker

[marker](https://github.com/VikParuchuri/marker)
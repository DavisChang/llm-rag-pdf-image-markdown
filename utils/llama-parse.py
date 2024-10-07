import os
from llama_parse import LlamaParse

# export LLAMA_CLOUD_API_KEY="llx-XXXXX"
LLAMA_CLOUD_API_KEY = os.environ["LLAMA_CLOUD_API_KEY"]
print(LLAMA_CLOUD_API_KEY)


def main():
    if not LLAMA_CLOUD_API_KEY:
        return

    documents = LlamaParse(result_type="markdown").load_data(
        "../assets/pdf/table/example.pdf"
    )

    print(documents)

    file_name = "pdf-to-markdown.md"
    all_text = ""
    for doc in documents:
        all_text += "\n\n" + doc.text
    with open(file_name, "w") as file:
        file.write(all_text)


if __name__ == "__main__":
    main()

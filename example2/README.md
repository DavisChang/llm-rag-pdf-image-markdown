# News

Local run need to download [Ollama](https://ollama.com/download)

Install open source models

```
ollama pull llama2
ollama pull mistral

# Serve the model as a REST API on locally
ollama serve
```

```
# Run to create vector database and add into database
python populate_database.py
python populate_database.py --reset

# Run it
python query_data.py "How do I get out of jail in Monopoly"

# Run test_rag.py
pytest
```

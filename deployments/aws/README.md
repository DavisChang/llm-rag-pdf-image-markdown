# Deploy Your RAG/AI App On AWS

- Python RAG/AI Applications: Proficiency in Python for building RAG systems or AI applications, leveraging various libraries and frameworks.
- FastAPI Library: Knowledge of FastAPI, a high-performance Python web framework, ideal for building APIs for machine learning and AI applications.
- Docker: Understanding of Docker for containerizing applications, ensuring portability and consistency across different environments.
- AWS and CDK (Cloud Development Kit): Familiarity with Amazon Web Services (AWS) and its CDK to deploy scalable AI applications on the cloud, automate infrastructure, and manage resources.


```bash
curl -X 'POST' \
  'http://localhost:8000/submit_query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query_text": "How much does a landing page for a small business cost?"
}'

docker build --platform linux/arm64/v8 -t aws_rag_app .
docker run --rm -it -p 8000:8000 --entrypoint python aws_rag_app app_api_handler.py
```

You can go to http://localhost:8000/ and http://localhost:8000/docs (Swagger)



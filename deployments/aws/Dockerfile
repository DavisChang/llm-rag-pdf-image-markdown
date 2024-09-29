FROM public.ecr.aws/lambda/python:3.11

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt --upgrade

# For local testing.
EXPOSE 8000

# Copy all files
COPY app_api_handler.py ${LAMBDA_TASK_ROOT}
COPY rag_app/* ${LAMBDA_TASK_ROOT}/rag_app
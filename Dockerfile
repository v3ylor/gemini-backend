FROM python:3.9-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Hugging Face expects port 7860 by default
EXPOSE 7860
CMD ["python", "app.py"]

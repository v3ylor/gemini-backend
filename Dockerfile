FROM python:3.9-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Tell HF which port to use
EXPOSE 7860
CMD ["python", "app.py"]

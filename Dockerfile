FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY src/ src/
COPY model/model.pkl model/model.pkl
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
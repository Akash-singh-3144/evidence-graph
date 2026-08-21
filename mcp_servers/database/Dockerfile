FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn pydantic asyncpg
COPY server.py /app/
EXPOSE 8003
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8003"]

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PORT=8000

WORKDIR /code

RUN apt-get update && apt-get install -y gcc libpq-dev net-tools && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["netstat", "-ntulp"]
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0"]

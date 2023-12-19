FROM python:3.11-slim


WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -e 'backend/src'

EXPOSE 8000

CMD ["uvicorn", "backend.src.rtvt_services.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

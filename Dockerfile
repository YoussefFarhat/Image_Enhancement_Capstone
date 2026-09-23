FROM python:3.11-slim
RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -v --extra-index-url https://download.pytorch.org/whl/cpu \
    torch torchvision
RUN pip install --no-cache-dir -v -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend
COPY BasicSR ./BasicSR

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
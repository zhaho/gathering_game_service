FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install xmltodict
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt ./
run pip install xmltodict
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD ["python3", "src/main.py"]
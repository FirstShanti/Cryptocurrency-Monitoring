FROM python:3.7

RUN mkdir -p /Kraken/

WORKDIR /Kraken/

COPY . /Kraken/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "kraken_aggregate.py"]

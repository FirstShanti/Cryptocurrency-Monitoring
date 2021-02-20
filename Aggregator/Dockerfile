FROM python:3.7

RUN mkdir -p /Aggregator/

WORKDIR /Aggregator/

COPY . /Aggregator/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "aggregate.py"]

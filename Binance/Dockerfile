FROM python:3.7

RUN mkdir -p /Binance/

WORKDIR /Binance/

COPY . /Binance/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "binance_aggregate.py"]

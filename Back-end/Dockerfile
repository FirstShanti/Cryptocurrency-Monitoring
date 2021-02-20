FROM python:3.8

RUN mkdir -p /Back-end/

WORKDIR /Back-end/

COPY . /Back-end/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn gevent

CMD gunicorn --worker-class gevent \
  --workers 4 \
  --bind :5000 \
  patched:app

EXPOSE 5000
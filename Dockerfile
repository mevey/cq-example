FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/flaskapp/src
#VOLUME ["/opt/services/flaskapp/src"]
# We copy the requirements.txt file first to avoid cache invalidations
COPY requirements.txt /opt/services/flaskapp/src/
WORKDIR /opt/services/flaskapp/src
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y sqlite3
COPY . /opt/services/flaskapp/src
RUN (cd /opt/services/flaskapp/src && rm -f cq_small.sqlite && gunzip -f --keep cq_small.sqlite.gz)
EXPOSE 5090
CMD ["python", "app.py"]

FROM python:3.10

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /opt/huefader
WORKDIR /opt/huefader
COPY huefader/* /opt/huefader/

RUN mkdir -p /root/.phue

WORKDIR /opt
ENTRYPOINT ["python3", "-m", "huefader"]

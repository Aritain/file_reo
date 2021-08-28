FROM    alpine:3.12.0
COPY    source/ /opt/source/

RUN apk --no-cache upgrade && \
    apk --no-cache add python3 py3-pip && \
    pip3 install --no-cache-dir -r /opt/source/requirements.txt

ENTRYPOINT ["python3", "/opt/source/main.py"]

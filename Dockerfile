FROM daocloud.io/python:3-onbuild
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN mkdir /www
WORKDIR /www
COPY . /www
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
EXPOSE 8000

CMD /www/docker-entrypoint.sh
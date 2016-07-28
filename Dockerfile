FROM daocloud.io/ubuntu
RUN apt-get update \ apt-get install python3
RUN apt-get install nginx
COPY nginx.conf /etc/nginx/nginx.conf
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN mkdir /www
WORKDIR /www
COPY . /www
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
EXPOSE 8000

CMD /www/docker-entrypoint.sh
FROM daocloud.io/nginx
RUN apt-get update
RUN apt-get -y install postgresql-server-dev-9.4
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -i http://pypi.douban.com/simple/ -r /tmp/requirements.txt
RUN mkdir -p /etc/nginx/sites-available/
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir /www
WORKDIR /www
COPY . /www
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
EXPOSE 80
VOLUME /www/log

CMD /www/docker-entrypoint.sh
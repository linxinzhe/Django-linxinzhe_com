FROM daocloud.io/ubuntu:14.04
RUN sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/mirrors.163.com\/ubuntu\//g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install nginx
COPY nginx.conf /etc/nginx/nginx.conf
RUN apt-get -y install postgresql
RUN apt-get -y install python3-pip
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
RUN mkdir /www
WORKDIR /www
COPY . /www
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
EXPOSE 8000

CMD /www/docker-entrypoint.sh
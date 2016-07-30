#!/bin/bash

docker build --tag linxinzhe_com .

docker run --name my-test-postgres -p 5432:5432 -e "POSTGRESQL_USERNAME=postgres" -e "POSTGRES_PASSWORD=" -e "POSTGRESQL_INSTANCE_NAME=postgres"  -d daocloud.io/postgres

docker run -p 8080:80 --link my-test-postgres:postgresql -e "POSTGRESQL_USERNAME=postgres" -e "POSTGRES_PASSWORD=" -e "POSTGRESQL_INSTANCE_NAME=postgres" --name linxinzhe_com linxinzhe_com
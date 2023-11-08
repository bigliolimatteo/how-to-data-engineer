FROM postgres:13

COPY  ./postgres/init-db.sql  /docker-entrypoint-initdb.d/
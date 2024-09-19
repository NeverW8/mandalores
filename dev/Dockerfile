FROM postgres:13.1

RUN apt-get update && apt-get install -y postgresql-13-postgis-3 postgresql-13-postgis-3-scripts

ENV POSTGRES_PASSWORD=mysecretpassword
ENV POSTGRES_USER=myuser
ENV POSTGRES_DB=mydatabase

CMD ["postgres"]


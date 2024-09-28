FROM ubuntu:latest

ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/mandalores

# Update package list and install required packages
RUN apt-get update && apt-get install -y \
    python3-full \
    python3-pip \
    python3-dev \
    build-essential \
    nginx \
    && apt-get clean


# Create application directory
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt $APP_HOME/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY mandalores $APP_HOME/mandalores
COPY manage.py $APP_HOME/
COPY run_nginx.sh $APP_HOME/
COPY assets $APP_HOME/assets
COPY nginx.conf /etc/nginx/nginx.conf

ENV ENV=production

EXPOSE 8080
ENV PATH="/opt/venv/bin:$PATH"
CMD ["/mandalores/run_nginx.sh"]

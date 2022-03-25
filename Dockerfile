
###################
# Builder Container #
###################
FROM python:3.9 as builder

WORKDIR /usr/src/app

## add and install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt



###################
# Final Container #
###################
FROM python:3.9-slim-buster

#RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install psycopg2 and other dependencies
RUN apt update && \
    apt upgrade -y && \
    apt install -y netcat-openbsd gcc libpq-dev && \
    apt install -y default-libmysqlclient-dev && \
    apt install -y tk && \
    apt install -y curl
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*


## add app
COPY . /usr/src/app
# RUN python manage.py collectstatic --no-input

CMD sh /usr/src/app/utils/run.sh
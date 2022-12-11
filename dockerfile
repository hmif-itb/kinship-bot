FROM python:3.7.16-slim-bullseye

ARG user=hmif

EXPOSE 8001

# as root
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN groupadd --gid 1001 ${user} && \
    useradd -g ${user} --uid 1001 -M ${user} && \
    mkdir -p /var/log/${user} && \
    chown ${user}:${user} /var/log/${user}
USER ${user}

CMD [ "gunicorn", "app:app", "--bind=0.0.0.0:8001" ]

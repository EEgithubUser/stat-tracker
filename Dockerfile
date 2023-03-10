FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install flask --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]
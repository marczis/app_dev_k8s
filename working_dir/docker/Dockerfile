FROM python:latest
WORKDIR /
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0 --workers=3" 
CMD gunicorn app
EXPOSE 8000

ADD app /app
RUN pip install -r /app/requirements.txt


FROM python:3.10-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN mkdir src
COPY ./src ./src
CMD gunicorn -b 0.0.0.0:80 --chdir src app:server

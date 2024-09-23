FROM python:3.8
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install -r requirements.txt
EXPOSE 9050:9050
ENTRYPOINT ["python"]
CMD ["main.py"]

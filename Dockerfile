FROM python:3.6-slim

WORKDIR /opt/apps
COPY . /opt/apps
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/opt/apps/src/app.py"]
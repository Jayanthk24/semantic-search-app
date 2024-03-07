FROM python:3.11
 
WORKDIR /app
 
COPY . /app
RUN pip install -r requirements.txt
ENV FLASK_ENV production
 
EXPOSE 3000
 
CMD ["python", "-u", "Flask-API-Endpoint.py"]
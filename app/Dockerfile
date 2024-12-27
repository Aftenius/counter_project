FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY wait-for-it.sh .
EXPOSE 5000
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "app.py"]
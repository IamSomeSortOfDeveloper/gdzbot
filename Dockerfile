FROM python:3.12.3
WORKDIR /app
COPY req.txt .
RUN pip install --no-cache -r /app/req.txt
COPY bot.py .
COPY . /app
CMD ["python", "bot.py"]
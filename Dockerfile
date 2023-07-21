# 
FROM python:3.11

# 
WORKDIR /app

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . .

#
ENV PORT=5000
EXPOSE 5000

# 
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]

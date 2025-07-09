FROM python:3.12

WORKDIR /ems

COPY ./requirements.txt /ems/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /ems/requirements.txt

COPY . /ems

CMD ["fastapi", "run", "/ems/app/main.py", "--port", "8000"]
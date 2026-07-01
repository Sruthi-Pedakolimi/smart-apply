FROM python:3.12

WORKDIR /smart-apply

COPY ./requirements.txt /smart-apply/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /smart-apply/requirements.txt

COPY ./ /smart-apply

CMD ["fastapi", "run", "main.py", "--port", "80"]



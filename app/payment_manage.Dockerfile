FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY ./payment_manage.py ./invokes.py c.
CMD [ "python", "./payment_manage.py" ]

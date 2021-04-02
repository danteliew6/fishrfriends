FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt amqp.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt 
RUN pip install --no-cache-dir -r amqp.reqs.txt
COPY ./payment_manage.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./payment_manage.py" ]

FROM python:3.9

LABEL maintainer="Jason Tsai <jason.tsaicc@gmail.com>"

RUN #apk add --no-cache gcc musl-dev libffi-dev openssl-dev

COPY . /tgi102_flask

WORKDIR /tgi102_flask

RUN pip3 install --upgrade pip && pip3 install gunicorn
RUN pip3 install -r requirements.txt
RUN chmod 755 run_server.sh

EXPOSE 8000

ENTRYPOINT [ "./run_server.sh" ]

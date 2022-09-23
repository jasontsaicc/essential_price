FROM python:3.9

LABEL maintainer="Jason Tsai <jason.tsaicc@gmail.com>"


RUN git clone https://github.com/EssentialTeam/-essential_price.git  && cd ./-essential_price && git checkout 6a3004e
WORKDIR ./-essential_price/tgi102_flask/
RUN pip install --upgrade pip
RUN apt-get update -y && apt-get install python3-pip -y && apt-get install vim -y
RUN pip3 install gunicorn  && chmod 755 ./run_server.sh
RUN pip3 install -r requirements.txt
RUN apt-get install wget && wget https://frankwubucket.s3.us-east-2.amazonaws.com/tflite_ResNetV2.tflite
RUN apt-get install libsm6 libxext6
#RUN pip uninstall opencv-python
#RUN pip uninstall opencv-python

EXPOSE 8000

ENTRYPOINT [ "./run_server.sh" ]

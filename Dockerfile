

# FROM gpuci/miniconda-cuda:11.1-runtime-centos7
FROM python:3.8.5

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
# ADD requirements.yaml /home/bin/requirements.yaml
# RUN conda env create -f /home/bin/requirements.yaml

RUN mkdir -p /home/project/
WORKDIR /home/project

EXPOSE "5000"
EXPOSE "6789"
EXPOSE "22"

CMD [ "bash" ]

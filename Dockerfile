

FROM gpuci/miniconda-cuda:11.1-runtime-centos7

ADD requirements.yaml /home/bin/requirements.yaml
RUN conda env create -f /home/bin/requirements.yaml

RUN mkdir -p /home/project/
WORKDIR /home/project


CMD [ "bash" ]

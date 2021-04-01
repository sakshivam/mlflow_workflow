

FROM gpuci/miniconda-cuda:11.1-runtime-centos7

# RUN apt-get update

# RUN apt-get install -y curl 
# RUN apt-get install python3.8 -y && apt-get install python3-pip && apt-get update
# RUN echo "alias python='/usr/bin/python3.8'" >> ~/.bashrc

ADD requirements.yaml /home/bin/requirements.yaml
RUN conda env create -f /home/bin/requirements.yaml

# RUN pip install -r requirements

RUN mkdir -p /home/project/
WORKDIR /home/project


ENV USER artinmajdi
ENV SHELL /bin/bash
ENV LOGNAME artinmajdi 


CMD [ "bash" ]
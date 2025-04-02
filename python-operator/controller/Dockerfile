FROM python:3.12
RUN pip install kopf
RUN pip install kubernetes
ADD . /src
CMD kopf run /src/sdz-controller.py --verbose
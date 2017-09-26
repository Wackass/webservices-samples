FROM python:2.7
WORKDIR /home
ADD requirements.txt test-requirements.txt ./
RUN pip install pylint
RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt
ENTRYPOINT ["/bin/bash"]

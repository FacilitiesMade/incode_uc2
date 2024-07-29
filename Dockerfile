FROM python:3.10.12-alpine3.18
RUN apk update ; apk upgrade
RUN mkdir /arkite_app
WORKDIR /arkite_app
COPY ./INCODE_UC2_Arkite.py ./INCODE_UC2_Arkite.py
COPY ./Requirements.txt ./Requirements.txt
RUN python -m pip install --upgrade pip wheel setuptools
RUN python -m pip install -r Requirements.txt
ENV FLASK_APP=INCODE_UC2_Arkite.py
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
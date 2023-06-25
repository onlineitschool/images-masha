FROM alpine:3.18.2

WORKDIR /flask

RUN apk add python3 py-pip

RUN pip install --upgrade pip

RUN python3 -m pip install --upgrade Pillow

RUN pip install flask

RUN apk add --no-cache gcc python3-dev musl-dev jpeg-dev zlib-dev

COPY ./ /flask/

CMD [ "python3", "/flask/resize.py" ]
FROM alpine:3.15.0

RUN apk add --no-cache tzdata

RUN cp -v /usr/share/zoneinfo/America/New_York /etc/localtime
RUN echo "America/New_York" > /etc/timezone

RUN apk add --no-cache font-noto mesa-dri-gallium py3-qt5 py3-pip py3-lxml py3-pillow python3

RUN pip install --upgrade pip
RUN pip install --upgrade labelimg google-api-python-client Pillow

COPY imgsearch.py /bin/imgsearch

ARG USER=labelimg

RUN addgroup $USER \
 && adduser -D -s /bin/sh -G $USER $USER \
 && echo "$USER:$USER" | chpasswd

USER $USER
RUN mkdir /home/$USER/imgs
WORKDIR /home/$USER/imgs



CMD ["labelImg"]


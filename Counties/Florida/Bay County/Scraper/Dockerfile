FROM python:3.8

RUN apt-get update && apt-get install -y \
  tesseract-ocr \
  libtesseract-dev

ENV APP_ROOT /scraper

# Set our working directory inside the image
WORKDIR $APP_ROOT

# Copy the app into place
COPY . .

# Install geckodriver
# Copied from: https://hub.docker.com/r/selenium/node-firefox/dockerfile
ARG GECKODRIVER_VERSION=0.26.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
  && chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver

RUN pip install -r requirements.txt

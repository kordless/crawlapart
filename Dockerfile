# Filename: Dockerfile
FROM python:3.7-slim-buster
WORKDIR /usr/src/app
RUN apt-get update \
&& apt-get install -y --no-install-recommends wget firefox-esr \
&& wget -qO- "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz" | tar xvz -C /usr/src/app

CMD ["/usr/src/app/geckodriver", "-v", "--host", "0.0.0.0"]

EXPOSE 4444

###############################################################################
# build and install dependencies stage
###############################################################################
FROM python:3.12-slim AS build

RUN apt-get update

WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

ARG dependencies="datatypes endpoints uvicorn"
RUN pip install --no-cache-dir ${dependencies}


###############################################################################
# app environment stage
###############################################################################
FROM python:3.12-slim

RUN groupadd -g 999 python && useradd -r -u 999 -g python python

WORKDIR /usr/app

COPY --chown=python:python --from=build /usr/app/venv ./venv

COPY --chown=python:python bounce ./bounce

USER 999

ENV PATH="/usr/app/venv/bin:$PATH"

#ARG BOUNCE_CONFIG
#ENV BOUNCE_CONFIG=${BOUNCE_CONFIG}


#CMD ["sleep", "infinity"]
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "4100", "bounce.__main__:application"]
HEALTHCHECK --interval=5m --start-period=5s --retries=3 \
  CMD python -c 'from urllib.request import urlopen; \
    exit(0 if urlopen("http://localhost:${PORT}/healthcheck").code == 200 else 1)'


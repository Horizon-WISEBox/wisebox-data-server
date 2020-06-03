FROM python:3.8.3-buster
ENV PYTHONUNBUFFERED 1
EXPOSE 80
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
      libpq-dev \
      netcat \
  && rm -rf /var/lib/apt/lists/* \
  && pip install pipfile-requirements \
  && mkdir /wiseparks
WORKDIR /wiseparks
ADD Pipfile.lock /wiseparks/
RUN pipfile2req Pipfile.lock > requirements.txt \
  && pip install -r requirements.txt \
  && rm requirements.txt Pipfile.lock \
  && wget https://raw.githubusercontent.com/eficode/wait-for/master/wait-for \
  && chmod a+x wait-for
ADD src /wiseparks/
ADD docker-entrypoint.sh /wiseparks
ENTRYPOINT [ "/wiseparks/docker-entrypoint.sh" ]

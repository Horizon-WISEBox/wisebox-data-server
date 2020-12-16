FROM python:3.8.3-buster
ENV PYTHONUNBUFFERED 1
EXPOSE 80
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
      libpq-dev \
      netcat \
  && rm -rf /var/lib/apt/lists/* \
  && pip install pipfile-requirements \
  && mkdir /wisebox
WORKDIR /wisebox
ADD Pipfile.lock /wisebox/
RUN pipfile2req Pipfile.lock > requirements.txt \
  && pip install -r requirements.txt \
  && rm requirements.txt Pipfile.lock \
  && wget https://raw.githubusercontent.com/eficode/wait-for/master/wait-for \
  && chmod a+x wait-for
ADD src /wisebox/
ADD docker-entrypoint.sh /wisebox
ENTRYPOINT [ "/wisebox/docker-entrypoint.sh" ]

FROM selenium/standalone-firefox

RUN sudo apt-get update -yqq \
    && sudo apt-get install -y --no-install-recommends apt-utils \
    && sudo apt-get install python3.7 -yqq \
    && sudo apt-get install python3-pip -yqq \
    && sudo apt-get install curl -yqq \
    && sudo apt-get install openssl \
    && pip3 install --upgrade pip \
    && pip3 install requests \
    && pip3 install selenium-wire \
    && pip3 install flask

ARG SELUSER_HOME=/home/seluser/scrapping_segs
ENV PYTHONPATH="${PYTHONPATH}:/home/seluser/scrapping_segs"
WORKDIR ${SELUSER_HOME}

COPY __init__.py __init__.py
COPY app.py app.py
COPY get_segment.py get_segment.py
COPY seg_config.ini seg_config.ini

ENV FLASK_APP app.py

RUN sudo chown -R seluser: ${SELUSER_HOME}

EXPOSE 5000

USER seluser

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
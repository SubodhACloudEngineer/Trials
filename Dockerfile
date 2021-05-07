FROM python:3.6.8
RUN set -x && \
    pip install netmiko==2.4.2 \
    nornir==2.3.0 \
    python-dotenv \
    tqdm && \
    git clone https://github.com/networktocode/ntc-templates.git
ENV NET_TEXTFSM=/ntc-templates/templates
WORKDIR /nornir
COPY . /nornir
VOLUME /nornir
ENTRYPOINT [ "/usr/local/bin/python" ]
LABEL version="0.1"

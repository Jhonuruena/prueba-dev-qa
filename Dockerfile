FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y \
        curl \
        wget \
        unzip \
        libglib2.0-0 \
        libnss3 \
        libfontconfig1 \
        libx11-xcb1 \
        libxtst6 \
        libxss1 \
        libdbus-1-3 \
        libgtk-3-0 \
        libasound2 \
        libgbm1 \
        libdrm2 \
        libxrandr2 \
        libpangocairo-1.0-0 \
        libatspi2.0-0 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
    && rm -rf /var/lib/apt/lists/*


RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir \
    pytest==8.4.1 \
    requests==2.32.4 \
    selenium==4.35.0 \
    pytest-html==4.0.0


RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.68/linux64/chrome-linux64.zip -O /tmp/chrome.zip && \
    unzip /tmp/chrome.zip -d /tmp && \
    mkdir -p /opt/chrome-linux64 && \
    mv /tmp/chrome-linux64/chrome /opt/chrome-linux64/chrome && \
    chmod +x /opt/chrome-linux64/chrome && \
    rm -rf /tmp/chrome*


RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.68/linux64/chromedriver-linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /tmp && \
    mkdir -p /opt/chromedriver-linux64 && \
    mv /tmp/chromedriver-linux64/chromedriver /opt/chromedriver-linux64/chromedriver && \
    chmod +x /opt/chromedriver-linux64/chromedriver && \
    rm -rf /tmp/chromedriver*


RUN wget -q https://github.com/grafana/k6/releases/download/v1.1.0/k6-v1.1.0-linux-amd64.tar.gz -O /tmp/k6.tar.gz && \
    tar -xzf /tmp/k6.tar.gz -C /tmp && \
    mv /tmp/k6-v1.1.0-linux-amd64/k6 /usr/local/bin/k6 && \
    chmod +x /usr/local/bin/k6 && \
    rm -rf /tmp/k6*

COPY . .

CMD ["python", "--version"]
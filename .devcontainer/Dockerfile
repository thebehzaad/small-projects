
# base image
FROM python:3.11-bullseye AS base

# Install system dependencies
RUN apt-get update -y \
 && apt-get install -y \
               wget \
               unzip \
               curl \
               libnss3 \
               libdbus-1-3 \
               libatk1.0-0 \
               libatk-bridge2.0-0 \
               libcups2 \
               libxcomposite1 \
               libxrandr2 \
               libxdamage1 \
               libxkbcommon0 \
               libgbm1 \
               libpango-1.0-0 \
               libasound2 \
               libwayland-client0 \
               libwayland-cursor0 \
               libwayland-egl1 \
               fonts-liberation \
               libcurl4 \
               xdg-utils \
 && rm -rf /var/lib/apt/lists/*

# Install Chrome from the specified URL
RUN wget -O /tmp/chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.165/linux64/chrome-linux64.zip && \
    unzip /tmp/chrome-linux64.zip -d /opt/chrome && \
    ln -s /opt/chrome/chrome-linux64/chrome /usr/bin/google-chrome && \
    rm /tmp/chrome-linux64.zip

# Install ChromeDriver from the specified URL
RUN wget -O /tmp/chromedriver-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.165/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver-linux64.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver-linux64.zip

    # set display port to avoid crash
ENV DISPLAY=:99

# Installing packages
RUN mkdir -p /home/analytics-user/wrkdir
COPY ./requirements-dev.txt /home/analytics-user/wrkdir
RUN python -m pip install -r /home/analytics-user/wrkdir/requirements-dev.txt


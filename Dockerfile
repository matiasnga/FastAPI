FROM python:3.10-slim
RUN apt-get update && \
    apt-get install -y wget fontconfig libfontconfig1 libfreetype6 libx11-6 libxext6 libxrender1 xfonts-75dpi xfonts-base libjpeg62-turbo fonts-liberation
RUN wget http://security.debian.org/debian-security/pool/updates/main/o/openssl/libssl1.1_1.1.1n-0+deb10u6_amd64.deb  && \
    dpkg -i /libssl1.1_1.1.1n-0+deb10u6_amd64.deb && \
    apt-get install -f

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6.1-2.bullseye_amd64.deb && \
    apt-get install -f
WORKDIR /app
COPY app app
COPY main.py .
COPY requirements.txt .

RUN pip install --upgrade setuptools
RUN pip install ez_setup
RUN pip install python-dotenv
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]


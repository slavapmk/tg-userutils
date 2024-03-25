FROM python
RUN apt-get update && \
    apt-get install -y tzdata locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" > /etc/timezone
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
COPY . /app
WORKDIR /app
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN ~/.local/bin/poetry install
CMD ~/.local/bin/poetry run userutils

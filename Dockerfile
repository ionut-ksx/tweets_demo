FROM python
RUN mkdir /app/
WORKDIR /app
RUN apt update && apt install zsh htop -y
RUN chsh -s /usr/bin/zsh
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
SHELL ["/bin/zsh", "-c"]

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
RUN pip install -e .

ENV FLASK_APP=app
ENV FLASK_ENV=development

RUN apt install -y ruby-full
RUN gem install --no-document  mailcatcher
CMD mailcatcher --ip 0.0.0.0 && cd /app/src/tweets_demo && gunicorn app:app --bind=0.0.0.0:5001 --workers=2
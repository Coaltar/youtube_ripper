FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY . /usr/src/app

COPY pyproject.toml ./

RUN pip install pdm 
RUN pdm install

# CMD ["pdm", "run", "python", "ripper_site/manage.py", "runserver", "0.0.0.0:8000"]
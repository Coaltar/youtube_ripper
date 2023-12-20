FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./ripper_site/ /usr/src/app

COPY pyproject.toml ./

RUN pip install pdm 
RUN pdm install

WORKDIR /usr/src/app/ripper_site

# CMD ["pdm", "run", "python", "ripper_site/manage.py", "runserver", "0.0.0.0:8000"]
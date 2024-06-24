FROM python:3.9

RUN useradd -m -u 1000 user
USER user

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN chown -R user:user /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY --chown=user:user . /code

CMD ["gunicorn", "-b", "0.0.0.0:7860", "main:app"]
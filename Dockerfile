FROM python:3.9

RUN useradd -m -u 1000 user
RUN mkdir -p /data
RUN chmod 777 /data
USER user
ENV TF_ENABLE_ONEDNN_OPTS = 0
ENV TF_CPP_MIN_LOG_LEVEL = 1
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY --chown=user . $HOME/app

CMD python3 -m flask run --host=0.0.0.0 --port=8000
EXPOSE 8000 
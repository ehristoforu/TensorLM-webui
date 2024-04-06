FROM python:3.10.14-bookworm

WORKDIR /home/app

RUN git clone https://github.com/ehristoforu/TensorLM-webui.git

WORKDIR /home/app/TensorLM-webui

RUN pip install -r requirements.txt

CMD [ "python", "webui.py" ]
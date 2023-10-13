FROM python:3.10

WORKDIR /front
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV BACKEND_URL http://back:8000

ENV APP_HOME /app
COPY . /front

# Intentionally do not expose port 8501 or else people can circumvent login

RUN pip install --no-cache-dir -r /front/requirements.txt

CMD streamlit run PDF_Researcher.py

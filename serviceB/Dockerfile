FROM python:3.7-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY serviceB/requirements.txt /requirements.txt
RUN pip install "--prefix=/install" -r /requirements.txt

#Final Image
FROM base
COPY --from=builder /install /usr/local
COPY serviceB/src/B.py /app/B.py

WORKDIR /app
CMD ["gunicorn", "-w 4", "B:app","-b","0.0.0.0:8082"]

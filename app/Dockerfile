# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.9 AS builder
EXPOSE 8000
WORKDIR /L7
ADD requirements.txt /L7
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt 
ADD . /L7 
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

FROM builder as dev-envs
RUN <<EOF

EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF

CMD ["manage.py", "runserver", "0.0.0.0:8000"]










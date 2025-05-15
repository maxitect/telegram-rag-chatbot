FROM python:3.13-slim

WORKDIR /app

COPY environment.yml .
RUN pip install PyYAML && \
    python -c "import yaml; deps = yaml.safe_load(open('environment.yml'))['dependencies']; [print(d) for d in deps if isinstance(d, str)]" > requirements.txt && \
    pip install $(cat requirements.txt | grep -v python=)

COPY . .

CMD ["python", "main.py"]
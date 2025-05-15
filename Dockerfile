FROM python:3.13-slim

WORKDIR /app

COPY environment.yml .
RUN pip install PyYAML && \
    python -c "import yaml; deps = yaml.safe_load(open('environment.yml'))['dependencies']; [print(d.replace('=', '==')) for d in deps if isinstance(d, str) and not d.startswith('python=')]" > requirements.txt && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
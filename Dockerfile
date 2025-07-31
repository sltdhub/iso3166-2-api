# Dockerfile
FROM public.ecr.aws/lambda/python:3.11

# Lambda Web Adapter extension
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter

WORKDIR /var/task
COPY . .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Your Flask app should listen on 0.0.0.0:8080
# If your index.py already runs app.run(host="0.0.0.0", port=8080) you're set.
ENV PORT=8080
ENV AWS_LWA_PORT=8080

# Start the app (you can swap for gunicorn if you prefer)
CMD ["python", "index.py"]

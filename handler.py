# handler.py
import aws_lambda_wsgi
from index import app  # import your existing Flask app object from index.py

def handler(event, context):
    # Translate the API Gateway (or Lambda Function URL/ALB) event into a WSGI request
    return aws_lambda_wsgi.response(app, event, context)

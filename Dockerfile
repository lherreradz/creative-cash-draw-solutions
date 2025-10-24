# Use AWS Lambda Python 3.9 base image
FROM public.ecr.aws/lambda/python:3.9

# Copy requirements and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy application code
COPY change_calculator.py currencies.py lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to the Lambda handler function
CMD [ "lambda_function.lambda_handler" ]
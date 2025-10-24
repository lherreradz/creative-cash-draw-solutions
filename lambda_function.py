import json
import boto3
import random
from io import StringIO
from change_calculator import calculate_change, process_file_content
from currencies import get_supported_currencies

def lambda_handler(event, context):
    """
    AWS Lambda handler function for change calculation.

    Supports both direct API calls and file processing.

    Args:
        event: Lambda event data
        context: Lambda context

    Returns:
        dict: Response with status code and body
    """
    try:
        # Extract currency from query parameters or default to USD
        currency = event.get('queryStringParameters', {}).get('currency', 'USD').upper()

        # Validate currency
        if currency not in get_supported_currencies():
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'Unsupported currency: {currency}',
                    'supported_currencies': get_supported_currencies()
                })
            }

        # Check if this is a file upload request
        if 'body' in event and event.get('body'):
            # Process file content
            file_content = event['body']
            output_content = process_file_content(file_content, currency)
            return {
                'statusCode': 200,
                'body': output_content,
                'headers': {
                    'Content-Type': 'text/plain',
                    'X-Currency': currency
                }
            }

        # Check if this is a single transaction request
        elif 'owed' in event and 'paid' in event:
            owed = event['owed']
            paid = event['paid']
            result = calculate_change(str(owed), str(paid), currency)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'owed': owed,
                    'paid': paid,
                    'currency': currency,
                    'change': result
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        else:
            # Return API documentation
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Creative Cash Draw Solutions - Change Calculator API',
                    'endpoints': {
                        'file_processing': {
                            'method': 'POST',
                            'body': 'file_content',
                            'query_params': {'currency': 'USD|EUR|COP'},
                            'response': 'processed_output'
                        },
                        'single_transaction': {
                            'method': 'POST',
                            'body': {'owed': 2.13, 'paid': 3.00},
                            'query_params': {'currency': 'USD|EUR|COP'},
                            'response': {'owed': 2.13, 'paid': 3.00, 'currency': 'USD', 'change': 'result'}
                        }
                    },
                    'supported_currencies': get_supported_currencies(),
                    'features': [
                        'Minimal change calculation',
                        'Random change when owed amount is divisible by 3',
                        'Multi-currency support (USD, EUR, COP)'
                    ]
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def process_file_content(file_content, currency='USD'):
    """
    Process file content and return results.

    Args:
        file_content (str): Content of the input file
        currency (str): Currency code

    Returns:
        str: Processed output content
    """
    output_lines = []
    for line_num, line in enumerate(StringIO(file_content), 1):
        line = line.strip()
        if not line:
            continue

        parts = line.split(',')
        if len(parts) != 2:
            output_lines.append(f"Error: Invalid line format on line {line_num}")
            continue

        owed_str, paid_str = parts
        result = calculate_change(owed_str.strip(), paid_str.strip(), currency)
        output_lines.append(result)

    return '\n'.join(output_lines)
# Creative Cash Draw Solutions - Change Calculator

A serverless application that calculates optimal change denominations for cashiers, with a creative twist: when the amount owed is divisible by 3, it generates random but valid change combinations.

## Features

- **Minimal Change**: Normally returns the minimum number of physical coins/bills
- **Random Twist**: When the owed amount is divisible by 3, generates random valid change combinations
- **Multi-Currency Support**: USD, EUR, and Colombian Peso (COP)
- **File Processing**: Accepts flat files with comma-separated owed and paid amounts
- **Error Handling**: Validates input and handles edge cases
- **AWS Deployment**: Serverless architecture using Lambda, API Gateway, and S3

## Supported Currencies

### USD (United States Dollar)

- $1 (100 cents)
- $0.25 (25 cents) - Quarter
- $0.10 (10 cents) - Dime
- $0.05 (5 cents) - Nickel
- $0.01 (1 cent) - Penny

### EUR (Euro)

- €2 (200 cents)
- €1 (100 cents)
- €0.50 (50 cents)
- €0.20 (20 cents)
- €0.10 (10 cents)
- €0.05 (5 cents)
- €0.02 (2 cents)
- €0.01 (1 cent)

### COP (Colombian Peso)

- $50,000
- $20,000
- $10,000
- $5,000
- $2,000
- $1,000
- $500
- $200
- $100
- $50

## Architecture

- **AWS Lambda**: Core change calculation logic
- **API Gateway**: RESTful endpoint for file uploads
- **S3**: Storage for input/output files
- **Python 3.9+**: Runtime environment

## API Usage

### Endpoint

```
POST /calculate-change
```

### Query Parameters

- `currency`: Currency code (USD, EUR, COP) - defaults to USD

### Request

Upload a text file with lines in format: `owed_amount,paid_amount`

Example file content:

```
2.13,3.00
2.14,3.00
5.00,5.00
```

### Response

Returns processed output with change breakdowns:

```
5 dimes, 36 pennies, 1 penny
3 quarters, 1 dime, 1 penny
No change owed
```

## Local Development

### Prerequisites

- Python 3.9+
- pip

### Setup

```bash
cd change_calculator
pip install -r requirements.txt
```

### Testing

```bash
python test_change_calculator.py
```

### Local Processing

```bash
python change_calculator.py
```

This processes `input.txt` and generates output files for all currencies.

## Algorithm Details

### Minimal Change

Uses greedy algorithm with currency-specific denominations.

### Random Change

When `owed_amount * 100 % 3 == 0`:

- Randomly selects valid combinations
- May use more coins than minimal
- Always sums to correct change amount

## Error Handling

- Invalid number formats
- Insufficient payment
- Malformed input lines
- Unsupported currencies

## Example Transactions

### USD Examples

| Owed | Paid | Change                      | Type                 |
| ---- | ---- | --------------------------- | -------------------- |
| 2.13 | 3.00 | Random combination          | Owed ÷ 3 = 71        |
| 2.14 | 3.00 | 3 quarters, 1 dime, 1 penny | Owed ÷ 3 = 71.333... |
| 5.00 | 5.00 | No change owed              | Exact payment        |

### EUR Examples

| Owed | Paid | Change                     | Type                 |
| ---- | ---- | -------------------------- | -------------------- |
| 2.13 | 3.00 | Random EUR combination     | Owed ÷ 3 = 71        |
| 2.14 | 3.00 | 1 euro, 50 cents, 36 cents | Owed ÷ 3 = 71.333... |

### COP Examples

| Owed | Paid | Change                 | Type                     |
| ---- | ---- | ---------------------- | ------------------------ |
| 1000 | 2000 | Random COP combination | Owed ÷ 3 = 333333.333... |
| 1500 | 2000 | 500 peso               | Owed ÷ 3 = 500000        |

## Deployment to AWS

### 1. Create Lambda Function

```bash
# Package the code
zip -r change-calculator.zip *.py

# Create Lambda function via AWS CLI or Console
aws lambda create-function --function-name change-calculator \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT-ID:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://change-calculator.zip
```

### 2. Create API Gateway

- Create REST API
- Add POST method
- Integrate with Lambda function
- Enable query parameter `currency`
- Enable CORS if needed

### 3. Configure S3 (Optional)

- Create buckets for input/output files
- Update Lambda to read from/write to S3

## Adding New Currencies

To add support for a new currency:

1. Add currency configuration to `currencies.py`:

```python
'NEW': {
    'name': 'New Currency',
    'symbol': 'N',
    'denominations': [
        ('100_unit', 10000),  # Value in smallest unit
        ('50_unit', 5000),
        # ... more denominations
    ]
}
```

2. Update the `format_denomination_name` function if needed for proper pluralization.

3. Test with the new currency code.

## License

This project is provided as-is for demonstration purposes.

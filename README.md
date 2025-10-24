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

### Built-in Currencies

#### USD (United States Dollar)

- $1 (100 cents)
- $0.25 (25 cents) - Quarter
- $0.10 (10 cents) - Dime
- $0.05 (5 cents) - Nickel
- $0.01 (1 cent) - Penny

#### EUR (Euro)

- €2 (200 cents)
- €1 (100 cents)
- €0.50 (50 cents)
- €0.20 (20 cents)
- €0.10 (10 cents)
- €0.05 (5 cents)
- €0.02 (2 cents)
- €0.01 (1 cent)

#### COP (Colombian Peso)

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

### Custom Currencies

You can upload your own custom currency definitions using plain text files. Use the provided `currency_template.txt` as a starting point.

#### Creating a Custom Currency

1. Copy `currency_template.txt` to create your currency file
2. Modify the following fields:

   - `CURRENCY_CODE`: Unique 3-10 character code (alphanumeric + underscore)
   - `CURRENCY_NAME`: Display name for your currency
   - `CURRENCY_SYMBOL`: 1-3 character symbol (e.g., $, €, £)

3. Define denominations using the format:

   ```
   DENOMINATION_NAME=VALUE_IN_SMALLEST_UNIT
   ```

   Example for a fictional currency:

   ```
   100_note=100000    # 100 unit note = 100,000 smallest units
   50_note=50000      # 50 unit note = 50,000 smallest units
   10_coin=10000      # 10 unit coin = 10,000 smallest units
   ```

#### Custom Currency File Format

```
# Currency Information
CURRENCY_CODE=YOUR_CODE
CURRENCY_NAME=Your Currency Name
CURRENCY_SYMBOL=$

# Denominations (from largest to smallest)
1000_note=100000
500_note=50000
100_note=10000
50_coin=5000
20_coin=2000
10_coin=1000
5_coin=500
1_coin=100
```

#### Validation Rules

- Currency code: 3-10 alphanumeric characters (+ underscore)
- Currency name: 1-50 characters
- Currency symbol: 1-3 characters
- Denominations: Positive integers, unique values, reasonable range (1-10,000,000)
- At least one denomination required

## Architecture

- **AWS Lambda**: Core change calculation logic
- **API Gateway**: RESTful endpoint for file uploads
- **S3**: Storage for input/output files
- **Python 3.9+**: Runtime environment

## API Usage

### Endpoints

#### Change Calculation

```
POST /calculate-change
```

**Query Parameters:**

- `currency`: Currency code (USD, EUR, COP, or custom) - defaults to USD

**Request:**
Upload a text file with lines in format: `owed_amount,paid_amount`

Example file content:

```
2.13,3.00
2.14,3.00
5.00,5.00
```

**Response:**
Returns processed output with change breakdowns:

```
5 dimes, 36 pennies, 1 penny
3 quarters, 1 dime, 1 penny
No change owed
```

#### Custom Currency Upload

```
POST /upload-currency
```

**Request:**
Upload a custom currency definition file (see format below)

**Response:**

```json
{
  "message": "Custom currency XYZ registered successfully",
  "currency_code": "XYZ",
  "currency_name": "Example Currency"
}
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

### Option 1: Traditional Zip Package Deployment

#### 1. Create Lambda Function

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

#### 2. Create API Gateway

- Create REST API
- Add POST method
- Integrate with Lambda function
- Enable query parameter `currency`
- Enable CORS if needed

### Option 2: Container Image Deployment (Recommended)

#### Prerequisites

- Docker installed
- AWS CLI configured
- ECR repository access

#### 1. Build and Push Container Image

Set your AWS environment variables:

```bash
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=your-account-id
```

Run the build script:

```bash
chmod +x build.sh
./build.sh
```

This will:

- Build the Docker image
- Authenticate with AWS ECR
- Create ECR repository (if needed)
- Push the image to ECR

#### 2. Deploy Lambda Function with Container

Run the deployment script:

```bash
chmod +x deploy.sh
./deploy.sh
```

This will:

- Create or update the Lambda function
- Use the container image from ECR
- Configure memory and timeout settings

#### 3. Create API Gateway

- Create REST API
- Add POST method for `/calculate-change`
- Add POST method for `/upload-currency`
- Integrate with Lambda function
- Enable query parameter `currency`
- Enable CORS if needed

#### 4. Test the Deployment

```bash
# Test change calculation
curl -X POST https://your-api-gateway-url/calculate-change?currency=USD \
  -H "Content-Type: text/plain" \
  -d "2.13,3.00"

# Test custom currency upload
curl -X POST https://your-api-gateway-url/upload-currency \
  -H "Content-Type: text/plain" \
  -d "CURRENCY_CODE=TEST\nCURRENCY_NAME=Test Currency\nCURRENCY_SYMBOL=@\n100_note=10000\n50_note=5000"
```

### Local Container Testing

Before deploying to AWS, test the container locally:

```bash
# Build the image
docker build -t change-calculator:latest .

# Run the container
docker run -p 9000:8080 change-calculator:latest

# Test with curl (in another terminal)
curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations \
  -d '{"body": "2.13,3.00"}'
```

### Environment Variables

For the deployment scripts, set these environment variables:

- `AWS_REGION`: Your AWS region (default: us-east-1)
- `AWS_ACCOUNT_ID`: Your AWS account ID

## Custom Currency API Usage

### Uploading a Custom Currency

1. Create a currency definition file using the template
2. Upload it via the `/upload-currency` endpoint
3. Use the returned currency code in change calculations

### Example Custom Currency Upload

**Request:**

```
POST /upload-currency
Content-Type: text/plain

CURRENCY_CODE=XYZ
CURRENCY_NAME=Example Currency
CURRENCY_SYMBOL=#
100_note=100000
50_note=50000
10_coin=10000
```

**Response:**

```json
{
  "message": "Custom currency XYZ registered successfully",
  "currency_code": "XYZ",
  "currency_name": "Example Currency"
}
```

### Using Custom Currency

**Request:**

```
POST /calculate-change?currency=XYZ
Content-Type: text/plain

10.50,20.00
```

**Response:**

```
1 100_note, 1 10_coin
```

## Adding Built-in Currencies

To add support for a new built-in currency:

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

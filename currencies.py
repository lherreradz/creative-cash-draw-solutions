"""
Currency configurations for the change calculator.
Each currency defines the available denominations in cents/centavos.
"""

# Global registry for custom currencies loaded at runtime
_CUSTOM_CURRENCIES = {}

CURRENCIES = {
    'USD': {
        'name': 'US Dollar',
        'symbol': '$',
        'denominations': [
            ('dollar', 100),
            ('quarter', 25),
            ('dime', 10),
            ('nickel', 5),
            ('penny', 1)
        ]
    },
    'EUR': {
        'name': 'Euro',
        'symbol': '€',
        'denominations': [
            ('2_euro', 200),
            ('1_euro', 100),
            ('50_cent', 50),
            ('20_cent', 20),
            ('10_cent', 10),
            ('5_cent', 5),
            ('2_cent', 2),
            ('1_cent', 1)
        ]
    },
    'COP': {
        'name': 'Colombian Peso',
        'symbol': '$',
        'denominations': [
            ('50000_peso', 50000),
            ('20000_peso', 20000),
            ('10000_peso', 10000),
            ('5000_peso', 5000),
            ('2000_peso', 2000),
            ('1000_peso', 1000),
            ('500_peso', 500),
            ('200_peso', 200),
            ('100_peso', 100),
            ('50_peso', 50)
        ]
    }
}

def get_currency_config(currency_code):
    """
    Get currency configuration by code.

    Args:
        currency_code (str): Currency code (USD, EUR, COP, or custom)

    Returns:
        dict: Currency configuration or None if not found
    """
    code = currency_code.upper()
    # Check built-in currencies first
    if code in CURRENCIES:
        return CURRENCIES[code]
    # Check custom currencies
    if code in _CUSTOM_CURRENCIES:
        return _CUSTOM_CURRENCIES[code]
    return None

def register_custom_currency(currency_code, currency_config):
    """
    Register a custom currency for use in calculations.

    Args:
        currency_code (str): Unique currency code
        currency_config (dict): Currency configuration

    Returns:
        bool: True if registered successfully, False otherwise
    """
    global _CUSTOM_CURRENCIES
    code = currency_code.upper()

    # Don't allow overwriting built-in currencies
    if code in CURRENCIES:
        return False

    _CUSTOM_CURRENCIES[code] = currency_config
    return True

def get_supported_currencies():
    """
    Get list of supported currency codes.

    Returns:
        list: List of supported currency codes (built-in + custom)
    """
    return list(CURRENCIES.keys()) + list(_CUSTOM_CURRENCIES.keys())

def parse_custom_currency_file(file_content):
    """
    Parse a custom currency definition file.

    Args:
        file_content (str): Content of the currency definition file

    Returns:
        dict: Currency configuration or None if parsing failed
    """
    try:
        lines = file_content.strip().split('\n')
        currency_info = {}
        denominations = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                if key == 'CURRENCY_CODE':
                    # Validate currency code (alphanumeric, 3-10 chars)
                    if not value or not value.replace('_', '').isalnum() or len(value) > 10:
                        return None
                    currency_info['code'] = value
                elif key == 'CURRENCY_NAME':
                    # Validate currency name (not empty, reasonable length)
                    if not value or len(value) > 50:
                        return None
                    currency_info['name'] = value
                elif key == 'CURRENCY_SYMBOL':
                    # Validate symbol (1-3 characters)
                    if not value or len(value) > 3:
                        return None
                    currency_info['symbol'] = value
                else:
                    # This is a denomination definition
                    try:
                        denom_value = int(value)
                        # Validate denomination value (positive, reasonable range)
                        if denom_value <= 0 or denom_value > 10000000:
                            continue
                        denominations.append((key, denom_value))
                    except ValueError:
                        continue

        # Validate required fields
        if not all(k in currency_info for k in ['code', 'name', 'symbol']):
            return None

        if not denominations:
            return None

        # Validate denominations (must have at least one, values must be unique)
        values = [d[1] for d in denominations]
        if len(values) != len(set(values)):
            return None  # Duplicate values

        # Sort denominations by value descending
        denominations.sort(key=lambda x: x[1], reverse=True)

        return {
            'name': currency_info['name'],
            'symbol': currency_info['symbol'],
            'denominations': denominations
        }

    except Exception:
        return None

def load_custom_currency(file_content):
    """
    Load a custom currency from file content.

    Args:
        file_content (str): Content of the currency definition file

    Returns:
        tuple: (currency_code, currency_config) or (None, None) if failed
    """
    config = parse_custom_currency_file(file_content)
    if config:
        # Generate a unique code if not provided or conflicts with built-in
        code = config.get('code', 'CUSTOM')
        if code in CURRENCIES:
            # Append timestamp or random suffix to make unique
            import time
            code = f"{code}_{int(time.time())}"

        return code, config
    return None, None

def format_denomination_name(name, count):
    """
    Format denomination name with proper pluralization.

    Args:
        name (str): Denomination name
        count (int): Count of denomination

    Returns:
        str: Formatted denomination string
    """
    # Handle special cases
    if name == 'penny':
        return f"{count} {'penny' if count == 1 else 'pennies'}"
    elif name == 'cent':
        return f"{count} {'cent' if count == 1 else 'cents'}"
    elif name == 'peso':
        return f"{count} {'peso' if count == 1 else 'pesos'}"
    elif '_' in name:
        # Handle compound names like '2_euro', '50_cent', '50000_peso'
        parts = name.split('_')
        if len(parts) == 2:
            value, unit = parts
            if unit in ['euro', 'cent', 'peso']:
                if count == 1:
                    return f"{value} {unit}"
                else:
                    if unit == 'cent':
                        return f"{count} {value} {unit}s"
                    elif unit == 'peso':
                        return f"{count} {value} {unit}s"
                    else:
                        return f"{count} {value} {unit}s"
    # Default pluralization
    if count == 1:
        return f"1 {name}"
    else:
        return f"{count} {name}s"
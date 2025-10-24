"""
Currency configurations for the change calculator.
Each currency defines the available denominations in cents/centavos.
"""

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
        currency_code (str): Currency code (USD, EUR, COP)

    Returns:
        dict: Currency configuration or None if not found
    """
    return CURRENCIES.get(currency_code.upper())

def get_supported_currencies():
    """
    Get list of supported currency codes.

    Returns:
        list: List of supported currency codes
    """
    return list(CURRENCIES.keys())

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
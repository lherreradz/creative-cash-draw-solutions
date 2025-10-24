import random
import math
from currencies import get_currency_config, format_denomination_name, get_supported_currencies

def calculate_change(owed_str, paid_str, currency='USD'):
    """
    Calculate the change denominations for a transaction.

    Args:
        owed_str (str): Amount owed as string (e.g., "2.13")
        paid_str (str): Amount paid as string (e.g., "3.00")
        currency (str): Currency code (USD, EUR, COP). Defaults to USD.

    Returns:
        str: Change breakdown or error message
    """
    try:
        owed = float(owed_str)
        paid = float(paid_str)
    except ValueError:
        return "Error: Invalid number format"

    if paid < owed:
        return "Error: Insufficient payment"

    # Get currency configuration
    currency_config = get_currency_config(currency)
    if not currency_config:
        return f"Error: Unsupported currency '{currency}'. Supported: {', '.join(get_supported_currencies())}"

    change_cents = round((paid - owed) * 100)

    if change_cents == 0:
        return "No change owed"

    # Check if owed amount is divisible by 3 (in cents)
    owed_cents = round(owed * 100)
    is_divisible_by_3 = (owed_cents % 3 == 0)

    if is_divisible_by_3:
        return calculate_random_change(change_cents, currency_config)
    else:
        return calculate_minimal_change(change_cents, currency_config)

def calculate_minimal_change(change_cents, currency_config):
    """
    Calculate change using minimal number of denominations.

    Args:
        change_cents (int): Change amount in cents
        currency_config (dict): Currency configuration

    Returns:
        str: Formatted change breakdown
    """
    result = []
    remaining = change_cents
    denominations = currency_config['denominations']

    for name, value in denominations:
        if remaining >= value:
            count = remaining // value
            remaining %= value
            result.append(format_denomination_name(name, count))

    return ", ".join(result)

def calculate_random_change(change_cents, currency_config):
    """
    Calculate change using random valid combinations of denominations.
    Allows more coins than minimal to create variety.

    Args:
        change_cents (int): Change amount in cents
        currency_config (dict): Currency configuration

    Returns:
        str: Formatted change breakdown
    """
    result = []
    remaining = change_cents
    denominations = currency_config['denominations']

    # Shuffle denominations for randomness
    shuffled_denoms = denominations.copy()
    random.shuffle(shuffled_denoms)

    # Use a greedy approach but with randomness
    for name, value in shuffled_denoms:
        if remaining > 0:
            # Randomly decide how many of this denomination to use (0 to remaining/value)
            max_count = remaining // value
            if max_count > 0:
                count = random.randint(0, max_count)
                if count > 0:
                    remaining -= count * value
                    result.append(format_denomination_name(name, count))

    # If we still have remaining cents, add the smallest denomination
    if remaining > 0:
        smallest_denom = denominations[-1]  # Last denomination is typically the smallest
        name, value = smallest_denom
        count = remaining // value
        if count > 0:
            result.append(format_denomination_name(name, count))

    # Sort result for consistent output order
    def sort_key(item):
        parts = item.split()
        denom_name = parts[1] if len(parts) > 1 else ""
        # Remove plural 's' for lookup
        if denom_name.endswith('s') and denom_name not in ['pennies', 'cents', 'pesos']:
            denom_name = denom_name[:-1]
        elif denom_name in ['pennies', 'cents', 'pesos']:
            denom_name = denom_name[:-3] + 'y' if denom_name == 'pennies' else denom_name[:-1]

        denom_dict = {name: i for i, (name, _) in enumerate(denominations)}
        return denom_dict.get(denom_name, 999)

    result.sort(key=sort_key)
    return ", ".join(result)

def process_file(input_file_path, output_file_path, currency='USD'):
    """
    Process input file and generate output file with change calculations.

    Args:
        input_file_path (str): Path to input file
        output_file_path (str): Path to output file
        currency (str): Currency code. Defaults to USD.
    """
    try:
        with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split(',')
                if len(parts) != 2:
                    outfile.write(f"Error: Invalid line format on line {line_num}\n")
                    continue

                owed_str, paid_str = parts
                result = calculate_change(owed_str.strip(), paid_str.strip(), currency)
                outfile.write(result + '\n')

    except FileNotFoundError:
        print(f"Error: Input file '{input_file_path}' not found")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    # Example usage with different currencies
    print("Testing USD:")
    process_file("input.txt", "output_usd.txt", "USD")

    print("Testing EUR:")
    process_file("input.txt", "output_eur.txt", "EUR")

    print("Testing COP:")
    process_file("input.txt", "output_cop.txt", "COP")
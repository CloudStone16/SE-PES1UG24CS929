import re

_WHOLE_NUMBER = re.compile(r"[0-9]+")


def _to_whole_number(token):
    """
    Returns token as a non-negative int, or None if it is not a plain run of
    ASCII digits (so '', 'abc', '-5', '1.5', '1_000' and '²' are all rejected).
    """
    token = token.strip()
    if not _WHOLE_NUMBER.fullmatch(token):
        return None
    try:
        return int(token)
    except ValueError:
        # Python refuses to convert absurdly long digit strings.
        return None


def clean_dish_name(name):
    """
    Removes the chef's-special markers (*, #, ~) and title-cases the name.
    Returns '' if name is not a string (e.g. None).
    """
    if not isinstance(name, str):
        return ""
    for ch in ['*', '#', '~']:
        name = name.replace(ch, '')
    return name.strip().title()


def parse_item_prices(text):
    """
    Parses comma-separated prices into a list of ints.
    Empty, non-numeric, negative or decimal entries are skipped, and a
    non-string input gives an empty list.
    """
    if not isinstance(text, str):
        return []
    prices = []
    for token in text.split(','):
        price = _to_whole_number(token)
        if price is not None:
            prices.append(price)
    return prices


def split_amount(text):
    """
    Splits 'TOTAL/PEOPLE' into the amount each person pays.
    Returns None if the input is not exactly two whole numbers separated by
    '/', or if people is zero.
    """
    if not isinstance(text, str):
        return None
    parts = text.split('/')
    if len(parts) != 2:
        return None
    total = _to_whole_number(parts[0])
    people = _to_whole_number(parts[1])
    if total is None or people is None or people == 0:
        return None
    return total // people


def main():
    print("==== Running clean_dish_name ====")
    value = input("Enter a dish name from the menu (e.g. *paneer tikka*): ")
    print("Dish name:", clean_dish_name(value))

    print("\n==== Running parse_item_prices ====")
    value = input("Enter item prices separated by commas (e.g. 250,180,320): ")
    print("Item prices:", parse_item_prices(value))

    print("\n==== Running split_amount ====")
    value = input("Enter the bill and number of people as TOTAL/PEOPLE (e.g. 1200/4): ")
    share = split_amount(value)
    if share is None:
        print("Invalid input: expected TOTAL/PEOPLE as whole numbers with at least 1 person.")
    else:
        print("Each person pays:", share)

if __name__ == "__main__":
    main()

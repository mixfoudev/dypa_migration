from datetime import datetime

def get_gender(value):
    if not value: return None
    if value.upper() == 'Α': return 'MALE'
    elif value.upper() == 'Θ': return 'FEMALE'
    else: return 'OTHER'

def get_date(date_string):
    """
    Ensures a date string is in 'YYYY-MM-DD' format.
    
    If the input date_string is already in 'YYYY-MM-DD' format, it returns it as is.
    If it's in 'DD/MM/YYYY' format, it converts it to 'YYYY-MM-DD'.
    For any other invalid or unrecognized format, it returns None.

    Args:
        date_string (str): The date string to check and convert.

    Returns:
        str or None: The date string in 'YYYY-MM-DD' format, or None if conversion fails.
    """
    if not date_string: return None

    if not isinstance(date_string, str):
        return None # Ensure input is a string

    # Attempt to parse as YYYY-MM-DD first
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return date_string  # It's already in the desired format
    except ValueError:
        pass # Not in YYYY-MM-DD, proceed to check other formats

    # Attempt to parse as DD/MM/YYYY
    try:
        date_object = datetime.strptime(date_string, "%d/%m/%Y")
        # If successful, convert it to YYYY-MM-DD
        return date_object.strftime("%Y-%m-%d")
    except ValueError:
        pass # Not in DD/MM/YYYY

    # If neither format matched, return None
    return None

def calc_period(tp):
    if not tp: return None
    if tp.upper() in ["Α", "Α'", "Α ΤΆΞΗ", "Α ΤΑΞΗ"]: return 1
    if tp.upper() in ["Β", "Β'", "Β ΤΆΞΗ", "Β ΤΑΞΗ"]: return 2
    return None
#
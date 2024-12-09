def clean_phone_number(phone):
    """
    Cleans and standardizes phone numbers to the format +254xxxxxxxxx.
    Removes spaces and validates the number format.
    """
    phone = phone.replace(' ', '').strip()  # Remove spaces
    if not phone.startswith('+254'):
        raise ValueError("Phone number must start with '+254'.")
    if len(phone) != 13:  # Check for the correct length
        raise ValueError("Phone number must be 13 characters, including '+254'.")
    return phone

import requests

def validate_npi(npi_number, first_name, last_name, state):
    """
    Validates a clinician's NPI number using the NPI registry API.
    We also validate that the name of the clinician matches the provided details.
    If not validated, we return False.
    
    Args:
        npi_number (str): The NPI number to validate.
        first_name (str): The clinician's first name.
        last_name (str): The clinician's last name.
        state (str): The state abbreviation where the clinician practices.

    Returns:
        bool: True if the NPI number is valid and matches the provided details, False otherwise.
    """
    url = "https://npiregistry.cms.hhs.gov/api/"
    params = {
        "version": "2.1",
        "number": npi_number,
        "first_name": first_name,
        "last_name": last_name,
        "state": state,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('result_count', 0) > 0:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error validating NPI number: {e}")
        return False
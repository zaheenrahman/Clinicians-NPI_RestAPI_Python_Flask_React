import requests

def validate_npi(npi_number, first_name, last_name, state):
    """
    Validates a clinician's NPI number using the NPI registry API.
    
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
        #"limit": 1
    }

    try:
        response = requests.get(url, params=params)
        print(response)
        response.raise_for_status()  # Raises a HTTPError if the response status code is 4XX or 5XX
        data = response.json()
        print(response)
        #https://npiregistry.cms.hhs.gov/api/?number=1679576722&enumeration_type=&taxonomy_description=&name_purpose=&first_name=&use_first_name_alias=&last_name=&organization_name=&address_purpose=&city=&state=&postal_code=&country_code=&limit=&skip=&pretty=on&version=2.1

        # Check if the response contains any results
        if data.get('result_count', 0) > 0:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error validating NPI number: {e}")
        return False
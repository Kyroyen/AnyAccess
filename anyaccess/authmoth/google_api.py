import requests
from exceptions.google_api_exceptions import GoogleAPITokenException

google_verification_endpoint = "https://oauth2.googleapis.com/tokeninfo?id_token="

required_fields = ["email", "email_verified", "name", "picture", "given_name", "family_name"]

def google_token_verify(access_token:str):
    req = requests.get(f"{google_verification_endpoint}{access_token}")

    res = req.json()
    # print(res)
    
    for i in required_fields:
        if i not in res: # type: ignore
            print(i)
            raise GoogleAPITokenException
    
    final_result = {k:res[k] for k in required_fields}
    
    # print(final_result)
        
    return final_result

#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from oauth_team.crew import OauthTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
backend_folder = 'output/authservice'
frontend_folder = 'output/authservice_ui'
backendunit_folder = 'output/authservice_unit_test'
connection_string = 'mongodb://localhost:27017/authservice'

os.makedirs(backend_folder, exist_ok=True)
os.makedirs(frontend_folder, exist_ok=True)
os.makedirs(backendunit_folder, exist_ok=True)

requirements = '1. Create a authentication service by collecting users email and password or by using social media login.\
    2. We need to make sure OAuth2 with PKCE challenge is implementded for authentication process as securiity best practice.\
    3. We need an front end ui to collect user email and password or social media login and passit on to back service.\
    4. User should be able to register, login and update there profile information.\
    5. User should be provided with auth token and refresh token after successful login.\
    6. Auth token should be valid for 10 min and refresh token should be valid for 6 Hours.\
    7. If user provides wrong email or password, backend service should provide a generic message with out providing much information regarding user name and password.\
    8. Password should be minimum of 8 character and should contain alphanumeric character and only $ and # as special characters.\
    9. User should be able to reset password by providing email and new password.'


def run():
    """
    Run the crew.
    """
    inputs = {
        'requirements': requirements,
        'connection_string': connection_string,
        'backend_folder': backend_folder,
        'frontend_folder': frontend_folder,
        'backendunit_folder': backendunit_folder       
    }
    
    try:
        results = OauthTeam().crew().kickoff(inputs=inputs)
        print(f"Results: {results.raw}")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")



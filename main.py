import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_cognito_users(user_pool_id):
    # Initialize a Cognito Identity Provider client
    client = boto3.client('cognito-idp')

    try:
        # Paginate through all users in the user pool
        paginator = client.get_paginator('list_users')
        page_iterator = paginator.paginate(UserPoolId=user_pool_id)

        for page in page_iterator:
            for user in page['Users']:
                username = user['Username']
                creation_date = user['UserCreateDate']
                print(f'Username: {username}, Creation Date: {creation_date}')

    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Incomplete credentials")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Replace with your Cognito User Pool ID
    user_pool_id = 'us-east-1_example'
    get_cognito_users(user_pool_id)

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

def get_cognito_users(user_pool_id):
    AWS_ACCESS_KEY_ID=os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY=os.environ["AWS_SECRET_ACCESS_KEY"]
    print(AWS_ACCESS_KEY_ID)
    print(AWS_SECRET_ACCESS_KEY)
    # Initialize a Cognito Identity Provider client
    client = boto3.client('cognito-idp')
    paginator = client.get_paginator("list_user_pools")

    # Create a PageIterator from the paginator
    page_iterator = paginator.paginate(MaxResults=10)

    # Initialize variables for pagination
    user_pools = []

    # Handle pagination
    for page in page_iterator:
        user_pools.extend(page.get("UserPools", []))

    # Print the list of user pools
    print("User Pools for the account:")
    if user_pools:
        for pool in user_pools:
            print(f"Name: {pool['Name']}, ID: {pool['Id']}, CreationDate: {pool["CreationDate"]}")
    else:
        print("No user pools found.")

if __name__ == '__main__':
    user_pool_id = 'us-west2'
    get_cognito_users(user_pool_id)

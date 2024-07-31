import boto3
import sqlite3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def initialize_db():
    conn = sqlite3.connect('cognito_users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_pool_id TEXT,
            username TEXT,
            creation_date TEXT
        )
    ''')
    conn.commit()
    return conn

def list_user_pools(client):
    try:
        user_pools = []
        response = client.list_user_pools(MaxResults=60)
        user_pools.extend(response['UserPools'])

        while 'NextToken' in response:
            response = client.list_user_pools(MaxResults=60, NextToken=response['NextToken'])
            user_pools.extend(response['UserPools'])

        return user_pools
    except Exception as e:
        print(f"An error occurred while listing user pools: {e}")
        return []

def list_users_in_pool(client, user_pool_id, cursor):
    try:
        paginator = client.get_paginator('list_users')
        page_iterator = paginator.paginate(UserPoolId=user_pool_id)

        for page in page_iterator:
            for user in page['Users']:
                username = user['Username']
                creation_date = user['UserCreateDate']
                cursor.execute('''
                    INSERT INTO users (user_pool_id, username, creation_date)
                    VALUES (?, ?, ?)
                ''', (user_pool_id, username, creation_date))
    except Exception as e:
        print(f"An error occurred while listing users in pool {user_pool_id}: {e}")

def main():
    # Initialize a Cognito Identity Provider client
    client = boto3.client('cognito-idp')

    try:
        # Initialize the database
        conn = initialize_db()
        cursor = conn.cursor()

        # List all user pools
        user_pools = list_user_pools(client)
        
        if not user_pools:
            print("No user pools found.")
            return

        # Iterate through each user pool and list users
        for pool in user_pools:
            user_pool_id = pool['Id']
            user_pool_name = pool['Name']
            print(f"\nUser Pool: {user_pool_name} (ID: {user_pool_id})")
            list_users_in_pool(client, user_pool_id, cursor)

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Incomplete credentials")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

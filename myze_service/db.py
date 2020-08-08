import boto3
import click
import os
import json
from flask.cli import with_appcontext

def get_db():
    return boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2', aws_access_key_id='test', aws_secret_access_key='test')

def get_client():
    return boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2', aws_access_key_id='test', aws_secret_access_key='test')


def delete_tables(dynamodb):
    tables = map(lambda t: t.name, dynamodb.tables.all())
    available_tables = ['Profiles']
    for table in available_tables:
        if table in tables:
            dynamodb.Table(table).delete()

def create_tables(dynamodb):
    dynamodb.create_table(
        TableName='Profiles',
        KeySchema=[
            {
                'AttributeName': 'PK',
                'KeyType': 'HASH'
            }, 
            {
                'AttributeName': 'SK',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PK',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SK',
                'AttributeType': 'S'
            },
            {
                'AttributeName': "User-Item-GSI",
                'AttributeType': 'S'
            },
            {
                'AttributeName': "Item-Size-GSI",
                'AttributeType': 'S'
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'User-Item-GSI',
                'KeySchema': [
                    {
                        'AttributeName': 'User-Item-GSI',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'PK',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            },
            {
                'IndexName': 'Item-Size-GSI',
                'KeySchema': [
                    {
                        'AttributeName': 'Item-Size-GSI',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'PK',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        StreamSpecification={
            'StreamEnabled': True,
            'StreamViewType': 'NEW_AND_OLD_IMAGES',
        }
    )
    
    
    with open('data.json', 'r') as datafile:
        data = json.load(datafile)

    client = get_client()

    # print (client.describe_table(TableName="Profiles"))

    for item in data:
        client.put_item(
            TableName="Profiles",
            Item=item
        )

@click.command('init-db')
@with_appcontext
def init_db_command():
    dynamodb = get_db()
    delete_tables(dynamodb)
    create_tables(dynamodb)
    click.echo('Initialized the database.')

def init_table():
    dynamodb = get_db()
    delete_tables(dynamodb)
    create_tables(dynamodb)
    print('Initialized the database for test.')

def init_app(app):
    app.cli.add_command(init_db_command)
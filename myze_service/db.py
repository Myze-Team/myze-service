import boto3
import click
from flask.cli import with_appcontext

def get_db():
    return boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')

def delete_tables(dynamodb):
    tables = dynamodb.list_tables()['TableNames']
    available_tables = ['Profiles']
    for table in available_tables:
        if table in tables:
            dynamodb.delete_table(TableName=table)

def create_tables(dynamodb):
    table = dynamodb.create_table(
        TableName='Profiles',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

@click.command('init-db')
@with_appcontext
def init_db_command():
    dynamodb = get_db()
    delete_tables(dynamodb)
    create_tables(dynamodb)
    click.echo('Initialized the database.')

def init_app(app):
    app.cli.add_command(init_db_command)
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.client('dynamodb','us-east-1')


def increment_page_visit_count():
    print ('******************Increment Page Count started*************************')
    try:
        dynamodb.describe_table(TableName='pagecount')
    except dynamodb.exceptions.ResourceNotFoundException:
        create_page_count_table()
    finally:
       print ('******************Increment Page Count ended*************************') 
    return  insert_page_count() 





def create_page_count_table():
    print ('***********Creating Table started******************')
    try:
        dynamodb.create_table(
                    TableName='pagecount',
                    KeySchema=[
                        { 'AttributeName': 'id', 'KeyType': 'HASH' } # partition key
                    ],
                    AttributeDefinitions=[
                        { 'AttributeName': 'id', 'AttributeType': 'N' }
                    ],
                    # Planning for capacity units
                    ProvisionedThroughput={ 'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1 }
            ) 
    # Wait until the table exists.
        dynamodb.get_waiter('table_exists').wait(TableName='pagecount')
    finally:
        print ('***********Creating Table ended******************')




def insert_page_count():
    print ('************Insert page count started************')
    try:
        response= dynamodb.update_item (
                TableName='pagecount',
                Key={
                        "id":{"N":"1"}
                    },
                UpdateExpression="SET #val = if_not_exists(#val,:zero) +:incr",
                ExpressionAttributeNames={ '#val': 'visitcount' },
                ExpressionAttributeValues={
                    ":incr" : {"N":"1"},
                    ":zero" :{"N":"0"}
                },
                ReturnValues='UPDATED_NEW'

        ) 
    except Exception as e:
        print(e)
    finally:
        print ('************Insert page count ended************')

    return response['Attributes']['visitcount']['N']


#print(increment_page_visit_count()['Attributes']['visitcount']['N'])

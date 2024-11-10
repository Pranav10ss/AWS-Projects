import json
import boto3
import os
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('http-crud-tutorial-items')

# Helper functions for DynamoDB operations
def get_item(item_id):
    try:
        response = table.get_item(Key={'id': item_id})
        return response.get('Item', {})
    except Exception as e:
        return str(e)

def get_all_items():
    try:
        response = table.scan()
        return response.get('Items', [])
    except Exception as e:
        return str(e)

def put_item(item_data):
    try:
        table.put_item(Item=item_data)
        return item_data
    except Exception as e:
        return str(e)

def delete_item(item_id):
    try:
        response = table.delete_item(Key={'id': item_id})
        return response
    except Exception as e:
        return str(e)

# Main handler function
def lambda_handler(event, context):
    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
    body = json.loads(event.get('body', '{}'))

    # GET /items/{id}
    if http_method == 'GET' and path.startswith('/items/') and path != '/items':
        item_id = path.split('/')[-1]
        item = get_item(item_id)
        return {'statusCode': 200, 'body': json.dumps(item)}

    # GET /items
    elif http_method == 'GET' and path == '/items':
        items = get_all_items()
        return {'statusCode': 200, 'body': json.dumps(items)}

    # PUT /items
    elif http_method == 'PUT' and path == '/items':
        if 'id' not in body:
            return {'statusCode': 400, 'body': json.dumps({'error': 'ID is required'})}
        item = put_item(body)
        return {'statusCode': 200, 'body': json.dumps(item)}

    # DELETE /items/{id}
    elif http_method == 'DELETE' and path.startswith('/items/'):
        item_id = path.split('/')[-1]
        response = delete_item(item_id)
        return {'statusCode': 200, 'body': json.dumps(response)}

    # Default response for unsupported methods
    return {'statusCode': 400, 'body': json.dumps({'error': 'Unsupported method'})}


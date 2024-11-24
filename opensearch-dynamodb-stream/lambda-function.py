import base64
import boto3
import json
import os
import re
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
from elasticsearch import helpers
from dynamodb_json import json_util as json

# Environment variables
HOST = os.environ.get('HOST')
INDEX = os.environ.get('ES_INDEX')
API_STAGE = os.environ.get('API_STAGE')
DB_HASH_KEY = os.environ.get('DB_HASH_KEY')
DB_SORT_KEY = os.environ.get('DB_SORT_KEY')

# Helper function to get ES client with AWS authentication
def get_es():
    session = boto3.Session()
    creds = session.get_credentials().get_frozen_credentials()
    access_key = creds.access_key
    secret_key = creds.secret_key
    session_token = creds.token

    awsauth = AWSRequestsAuth(
        aws_access_key=access_key,
        aws_secret_access_key=secret_key,
        aws_token=session_token,
        aws_host=HOST,
        aws_region=session.region_name,
        aws_service='es'
    )

    return Elasticsearch(
        hosts=[{'host': HOST, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

# Push data to Elasticsearch (OpenSearch)
def pushBatch(actions):
    elasticsearch = get_es()
    print('Pushing batch of: ' + str(len(actions)) + ' to ES')
    success, failed = helpers.bulk(elasticsearch, actions, stats_only=True)
    print('Batch successfully pushed to Elasticsearch')

# DynamoDB Stream processing function
def handle_dynamodb_event(event):
    try:
        eventTypes = ['INSERT', 'MODIFY', 'REMOVE']
        records = event['Records']
        actions = []
        ignoredRecordCount = 0
        
        for record in records:
            if record['eventName'] in eventTypes:
                action = json.loads(record['dynamodb']['OldImage']) \
                    if record['eventName'] == 'REMOVE' \
                    else json.loads(record['dynamodb']['NewImage'])
                actions.append(
                    {
                        '_index': INDEX,
                        '_type': '_doc',
                        '_id': action[DB_HASH_KEY] + ':' + action[DB_SORT_KEY],
                        '_source': action,
                        '_op_type': 'delete' if record['eventName'] == 'REMOVE' else 'index'
                    }
                )
            else:
                ignoredRecordCount += 1
                print(record)
            if len(actions) == 50:
                pushBatch(actions)
                actions = []

        if len(actions) > 0:
            pushBatch(actions)
        print('Invalid Event records ignored: ' + str(ignoredRecordCount))

    except Exception as e:
        print(f"Error in DynamoDB event processing: {e}")
        raise

# Function to handle the API Gateway proxy to OpenSearch requests
def handle_api_gateway_event(event):
    try:
        path = event.get('path')
        method = event.get('httpMethod')
        body = event.get('body')
        query_params = event.get('queryStringParameters')
        headers = event.get('headers', {})
        req_headers = {}
        
        for k, v in headers.items():
            if any(h in k for h in ['content-type', 'cookie', 'kbn-', 'osd-']):
                req_headers[k] = v
                
        opts = {
            'method': method.upper(),
            'HOST': HOST,
            'url': 'https://{}{}'.format(HOST, path),
            'service': 'es',
            'region': 'us-east-1',
            'headers': req_headers,
            'body': body,
            'params': query_params
        }

        auth = get_aws4auth(opts)
        req_headers.update(auth)

        response = requests.request(
            method=method,
            url='https://{}{}'.format(HOST, path),
            headers=req_headers,
            data=body,
            params=query_params,
            stream=True
        )

        (headers, body, isBase64Encoded) = format_response(response)

        return {
            'statusCode': response.status_code,
            'body': body,
            'headers': headers,
            'isBase64Encoded': isBase64Encoded
        }

    except Exception as e:
        print(f"Error in API Gateway event handling: {e}")
        raise

# Helper function to format API response
def format_response(response):
    resp_body = []
    headers = {}
    isBase64Encoded = False
    rewrite = {
        '&quot;_dashboards&quot': '&quot;{}/_dashboards&quot'.format(API_STAGE),
        '/_dashboards': '/{}/_dashboards'.format(API_STAGE)
    }

    h = dict(response.headers)
    del h['Connection']
    del h['Content-Length']
    if 'content-encoding' in h:
        del h['content-encoding']
    for k, v in h.items():
        headers[k.lower()] = v

    for content in response.iter_content(1024):
        if content:
            resp_body.append(content)
    resp_body = b''.join(resp_body)

    if any(h in headers['content-type'] for h in ['text', 'javascript']):
        resp_body = str(resp_body, 'utf-8')
    elif 'json' in headers['content-type']:
        resp_body = resp_body.decode('utf8').replace("'", '"')
    else:
        isBase64Encoded = True
        resp_body = str(base64.b64encode(resp_body))

    for k, v in rewrite.items():
        resp_body = resp_body.replace(k, v)

    return (headers, resp_body, isBase64Encoded)

# Helper function to get AWS4 authentication headers for OpenSearch requests
def get_aws4auth(opts):
    session = boto3.Session()
    creds = session.get_credentials().get_frozen_credentials()
    service = 'es'
    awsauth = AWSRequestsAuth(
        aws_access_key=creds.access_key,
        aws_secret_access_key=creds.secret_key,
        aws_token=creds.token,
        aws_host=opts['HOST'],
        aws_region=session.region_name,
        aws_service=service
    )   

    req = requests.Request(
        opts['method'],
        opts['url'],
        headers=opts['headers'],
        data=opts['body'],
        params=opts['params']
    )
    prepped = req.prepare()

    auth = awsauth.get_aws_request_headers(prepped,
                                aws_access_key=creds.access_key,
                                aws_secret_access_key=creds.secret_key,
                                aws_token=creds.token)

    return auth

# Main Lambda handler function
def lambda_handler(event, context):
    print("Incoming event:", json.dumps(event))

    try:
        if 'Records' in event:
            # DynamoDB Stream event
            print("Processing DynamoDB Stream event...")
            handle_dynamodb_event(event)
        elif 'httpMethod' in event:
            # API Gateway event
            print("Processing API Gateway event...")
            return handle_api_gateway_event(event)
        else:
            raise ValueError("Unsupported event source")

    except Exception as e:
        print(f"Error handling event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error')
        }


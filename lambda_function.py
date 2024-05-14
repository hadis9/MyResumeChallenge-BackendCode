import boto3

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('VisitorCounterTable')
tableName = 'VisitorCounterTable'


def lambda_handler(event, context):
    print(event)
    body = {}
    statusCode = 200

    try:
        if event['routeKey'] == "GET /items":
            response = table.get_item(Key={'VisitorID':0})
            if 'Item' in response:
                item = response['Item']['value']
            else:
                item = 0
            body = 'The number of visitors is ' + str(item)
        elif event['routeKey'] == "PUT /items":
            response = table.get_item(Key={'VisitorID': 0})
            print(response)
            if 'Item' in response:
                body = int(response['Item']['value']) + 1
            else:
                body = 1
                
            table.put_item(Item={'VisitorID':0,'value': body})
            body = 'Visitor number ' + str(body)
            
    except KeyError:
        statusCode = 400
        body = 'Unsupported route: ' + event['routeKey']
    return body

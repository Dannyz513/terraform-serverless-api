import json
import boto3
import os
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    http_method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    try:
        if http_method == "POST":
            body = json.loads(event.get("body") or "{}")
            item_id = str(uuid.uuid4())
            item = {"id": item_id, "content": body.get("content", "")}
            table.put_item(Item=item)
            return response(201, item)

        elif http_method == "GET":
            items = table.scan().get("Items", [])
            return response(200, items)

        else:
            return response(405, {"error": "Method not allowed"})

    except Exception as e:
        return response(500, {"error": str(e)})


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
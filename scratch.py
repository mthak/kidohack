from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
from flask import Flask, request, jsonify, abort
import logging
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table('gameusers')
try:
   data  =  table.get_item(Key={"rollnumber": "1000"})
except ClientError:
   raise Exception("Key Not Found")
print(data)
data = table.scan(FilterExpression=Attr('deviceid').eq('Da1023'))
if not data['Items']:
   print("Hello")
print(data)

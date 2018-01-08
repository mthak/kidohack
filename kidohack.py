from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
from flask import Flask, request, jsonify, abort
import logging
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

app = Flask(__name__)


def create_connection():
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table('gameusers')
    return table

@app.route('/getkid', methods=['POST'])
def get_child_data():
    table = create_connection()
    ''' method expects data in format {'rollnuber': "abc" , "device_id": "da123" }'''
    print("request is ", request)
    kiddata= request.get_json()
    print("data i got is ", kiddata)
    #logging.debug("Received data %" %(kiddata))
    if 'rollnumber' in kiddata:
        try:
            data = table.get_item(
                Key={
                    'rollnumber': kiddata['rollnumber'],
                })
        except KeyError:
            return("Invalid Key Found")
        print(data['Item'])
        if data['Item'] is None:
            data = {}
            data['Item'] = {"empty": True}
    else:
        try:
            print("Entering data for deviceid section")
            deviceid = kiddata['deviceid']
            print(" deviceid found is ", deviceid)
            data  = table.scan(FilterExpression=Attr('deviceid').eq(deviceid))
            print(data)
            if not data['Items']:
               data['Item'] = {"empty": True}
            else:
                 return json.dumps(data['Items'][0])
        except ClientError,KeyError:
              raise Exception("Device id not found in json")
    return json.dumps(data['Item'])


@app.route('/addkid', methods=['POST'])
def add_child_data():
    table = create_connection()
    kidjson = request.get_json()
    logging.debug("Received kids data json", kidjson)
    if not kidjson['deviceid']:
        raise Exception("Device Id not found")
        return "Sorry Invalid Data please try again"
    if not kidjson['name']:
        raise Exception("Expecting Kids name in response")
        return "Sorry Invalid Data please try again"
    if not kidjson['rollnumber']:
        raise Exception("Kids Pin not found")
        return "Sorry Invalid Data please try again"
    try:
        data = table.put_item(Item=kidjson)
        print("response from adding kid is ", data)
        if data['ResponseMetadata']['HTTPStatusCode'] == 200:
           return "User added Successfully"
    except all:
        return "Someting went wrong let's try again"

    raise Exception("Data not stored in database, Let's try again")


@app.route('/getquestion', methods=['POST'])
def get_questions():
    data = request.get_json()
    gradeinfo = data['gradeinfo']
    index = data['index']
    print("Retrieved data from imput", gradeinfo, index)
    json_data = open('mathdb.json').read()
    mathdb = json.loads(json_data)
    print(mathdb)
    for grade, questions in mathdb.iteritems():
        if gradeinfo in grade:
            print("Getting data for grade", grade, questions[0])
            if index < len(questions):
               print("Here is your question %s", questions[index]['ques'])
               return json.dumps(questions[index])
            else:
                 return("Well Done you completed all questions for today")

@app.route('/updatescore', methods=['POST'])
def update_score():
    table = create_connection()
    data = request.get_json()
    rollnumber = data['rollnumber']
    points = data['points']
    dbdata = table.get_item(Key={'rollnumber': rollnumber})
    print("Retrieved data for kid as ", dbdata['Item'])
    if 'points' in json.dumps(dbdata['Item']):
        print("kid has existing points in db", dbdata['Item']['points'])

        points += int(dbdata['Item']['points'])
        data['points'] = points
    else:
        data['points'] = points
    print("updated record set is ", data)
    table.update_item(Key={'rollnumber':rollnumber},
                      UpdateExpression="set points = :p",
                      ExpressionAttributeValues={ ':p' : str(points)},
                      ReturnValues="UPDATED_NEW")
    return "Record updated successfully"

if __name__ == "__main__":
    LOG_FORMAT = '[%(asctime)s] %(process)d %(module)-12s %(levelname)-8s %(message)s'
    DATE_FORMAT = '%d/%b/%Y %H:%M:%S %z'
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT, datefmt=DATE_FORMAT)
    app.run(host="0.0.0.0", port=7080, threaded=True)

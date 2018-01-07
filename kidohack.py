from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
from flask import Flask, request, jsonify, abort
app = Flask(__name__)

def create_connection():
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table('gameusers')

@app.route('/getkid', methods=['GET'])
def get_child_data():
    data = request.get_json()
    if rollnumber in data['rollnummber']:
       try:
          data = table.get_item(
            Key={
                'rollnumber': rollnumber,
               })
       except KeyError:
          return("Invalid Key Found")
       print(data['Item'])
       if data['Item'] is None:
          data = {"empty": True}
          return data
       return data['Item']
    else:
      deviceid = data['deviceid']
      try:
         data = table.get_item(key='deviceid' = deviceid})
         print data
         return data['Item']
         if data['Item'] is None:
            data = {"empty": True}
            return data


@app.route('/addkid', methods=['POST'])
def add_child_data():
    kidjson = request.get_json()
    logging.debug("Received json", kidjson)
    if not kidjson('deviceid'):
       raise Exception("Device Id not found")
       return "Sorry Invalid Data please try again"
    if not kidjson('name'):
       raise Exception("Expecting Kids name in response")
       return "Sorry Invalid Data please try again"
    if not kidjson('pin'):
       raise Exception("Kids Pin not found")
       return "Sorry Invalid Data please try again"
    try:
      table.put_item(Item={kidjson})
    except e:
      raise Exception("Data not stored in database, Let's try again")

@app.route('/getquestion', methods=['GET'])
def get_questions():
    data = request.get_json()
    gradeinfo = data['gradeinfo']
    index = data['index']
    with open('mathdb.json') as json_data:
        mathdb = json.loads(json_data)
    for grade,questions in mathdb.iteritems:
        if gradeinfo in grade:
           for data in questions[index]:
               print("Here is your question %s", data['ques'])
               return data

@app.route('/updatescore', methods=['POST'])
def upate_score():
    data = request.get_json()
    rollnumber = data['rollnumber']
    points = data['points']
    data = table.get_item(key={'rollunmber':rollnumber})
    if data['score']:
       score = data['score']
       score = score+points
       data['score'] =score
    else:
       data['score'] = points
    data.put_item(data)



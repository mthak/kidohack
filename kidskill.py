import requests
from flask import Flask, render_template
import gettext
from flask_ask import (
                       Ask,
                       request as ask_request,
                       session as ask_session,
                       statement,
                       question as ask_question
                       )


app = Flask(__name__)
ask = Ask(app, "/")
ASK_APPLICATION_ID = "amzn1.ask.skill.00125890-0644-49fd-a5dd-2825979440a5"
app.config['ASK_VERIFY_REQUESTS'] = False



@ask.intent('AddKid')
def create_user():
    user = {}
    child_name = ask_request.intent.slots.SignUpName.value
    child_id = ask_request.intent.slots.SignUpId.value
    deviceid = ask_request.Amazon.deviceId
    user['rollnumber'] = child_id
    user['name'] = child_name
    user['deviceid'] = deviceid
    response = request.put("http://localhost:5000/addkid", data=user)
    if response.status_code == 200:
       return("Welcome"+child_name+"to the family of MathGoodies")
    return statement(text)


@ask.intent('Hello')
def get_kidsdata():
    userjson ={}
    deviceid = ask_request.deviceid
    userjson['deviceid'] = deviceid
    response = request.get("http://localhost:5000/getkid", data = userjson)
    if response.status_code == 200:
       kidsdata = response.get_json()
       if empty in json:
          return("Looks like you are a new user to our MathGoodies Family, Welcome ")
       else:
           if len(kidsdata) > 1:
           kidsuser = []
           for data in kidsdata:
               print data['name']
               kidsuser.append(data['name'])
           return("Welcome I found " + len(kidsdata)+ " users with this device" reprompt =" Please tell us your personalized key")
           rollnumber = ask_request.intent.slots.child_id.value
           userdata = {'rollnumber' = rollnumber}
           response = request.post("http://localhost:5000/getkid", data= userdata)
           if response.get_status == 200:
              kidsuser = reponse.json()['name']
              return("Welcome" + kidsuser + "Ready for some fun and more goodies" repro>  \mpt = " Tell me which grade you are in ")
           else:
                kidsuser = kidsdata['name']
                return("Welcome" + kidsuser + "Ready for some fun and more goodies" reprompt = " Tell me which grade you are in ")
                gradeinfo = ask_request.intent.slots.gradeInfo.value

def ask_question(gradeinfo):
    userdata = {}
    userdata['gradeinfo'] = gradeinfo
    userdata[index] = index
    response = request.get("http://localhost:5000/getkid", data = userdata)
    if response.get_status == 200:
       quesdata = response.get_json()
       return("Here is your Question" + quesdata['ques']
       answer = ask_request.intent.slots.answer.value
       if quesdata['answer'] = answer:
          points = quesdata['points']
          data = {}
          data['points'] = points
          data['rollnumber'] = child_id
          reponse = request.post("http://localhost:5000/update_score", data = data)
          if response.get_status == 200:
             score = response.get_json()['score']
             return("Your score is updated. You new score is " + score)
             reprompt("Ready for new Question ?")
             newquestion = ask_request.intent.slots.newquestion.value
             if newquestion == "Yes":
                index = index+1
                ask_question()

if __name__ == '__main__':
    app.run(debug=True)


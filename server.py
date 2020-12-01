import flask
from flask import request, jsonify
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import os
load_dotenv()


app = flask.Flask(__name__)
app.config['DEBUG'] = True

def auth(): 
    authenticator = IAMAuthenticator(os.getenv('API_KEY'))
    assistant = AssistantV2(
        version='2020-09-24',
        authenticator=authenticator
    )
    assistant.set_service_url(os.getenv('URL'))
    return assistant 

@app.route('/api/v1/session', methods=['GET'])
def create_session(): 
    assistant = auth()

    response = assistant.create_session(
        assistant_id=os.getenv('ASSISTANT_ID')
    ).get_result()
    
    if 'session_id' in response:
        response['success']=True
        return jsonify(response), 200
    else: 
        return jsonify(success=False)


@app.route('/api/v1/message', methods=['POST'])
def send_message():
    assistant = auth()

    response = assistant.message(
        assistant_id=os.getenv('ASSISTANT_ID'),
        session_id=request.headers.get('session_id'),
        input={
            'message_type': 'text',
            'text': request.json['user_message']
        }
    ).get_result()

    if 'output' in response:
        response['success']=True
        resp = {
            "success": True,
            "response": response['output']['generic'][0]['text']
        }

        return jsonify(resp)
    else: 
        return jsonify(success=False)


app.run()
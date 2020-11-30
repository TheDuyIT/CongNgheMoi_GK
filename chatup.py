from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid
app = Flask(__name__)

#app.config[ 'SECRET_KEY' ] = ''
socketio = SocketIO( app )

keys = {
	'ACCESS_KEY_ID' : '',
	'ACCESS_SECRET_KEY' : '',
    'REGION_NAME' : ''
}
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=keys['ACCESS_KEY_ID'],
                          aws_secret_access_key=keys['ACCESS_SECRET_KEY'],
                          # aws_session_token=keys.AWS_SESSION_TOKEN
                          region_name= keys['REGION_NAME']
                          )




@app.route( '/' )
def hello():
  return render_template( './ChatApp.html' )




def messageRecived():
  print( 'message was received!!!' )


@socketio.on( 'my eventes' )
def handle_my_custom_event1( json1 ):

  import chatbot_final
  message = json1['message']
  answer=chatbot_final.chat(message)
  table = dynamodb.Table('chatbots')

  table.put_item(
      Item={    
                'ID' : str(uuid.uuid4()),
                'message': message,
                'answer': answer,
            }
        )

  json1['answer'] = answer
  json1['bot']='AdhocBot'
  print( 'recived my event: ' + str(json1 ))
  socketio.emit( 'my response', json1, callback=messageRecived )

if __name__ == '__main__':
  socketio.run( app, host = '0.0.0.0', port = 8080, debug = True )

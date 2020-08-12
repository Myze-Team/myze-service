import json


def lambda_handler(event, context):
    print (dir(context))
    print (context.name)
    print ("lmaoefoaejfiae")
    print (event)
    for record in event['Records']:
        print('EventID: ' + record['eventID'])
        print('EventName: ' + record['eventName'])
    print('Successfully processed %s records.' % str(len(event['Records'])))

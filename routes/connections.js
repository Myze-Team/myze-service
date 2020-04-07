require('dotenv').config()
const AWS = require('aws-sdk')
const uuidv4 = require('uuid/v4');
const router = require('express').Router()
const isEmpty = require('is-empty')

AWS.config.update({
  region: 'us-west-2',
  endpoint: process.env.DB_ENDPOINT,
})

const docClient = new AWS.DynamoDB.DocumentClient()

const getConnections = () => {
  const params = {
    TableName: 'Connection',
    ProjectionExpression: '#id, #userId, #clothingId, #brand, #type, #name',
    ExpressionAttributeNames: {
      '#id': 'id',
      '#userId': 'userId',
      '#clothingId': 'clothingId',
      '#size': 'size',
      '#cost': 'cost',
      '#timeObtained': 'timeObtained',
      '#fit': 'fit',
    }
  }

  console.log('[NOTE] Scanning Connection table')
  docClient.scan(params, onScan)

  function onScan(err, data) {
    if (err) {
      console.error('Unable to scan the table. Error JSON:', JSON.stringify(err, null, 2))
    } else {
      // log the queried elements
      console.log('[NOTE] Scan succeeded');
      data.Items.forEach((connection) => console.log(connection.id))

      if (typeof data.LastEvaluatedKey != 'undefined') {
        console.log('[NOTE] Scanning for more...')
        params.ExclusiveStartKey = data.LastEvaluatedKey
        docClient.scan(params, onScan)
      }
    }
  }
}

const createConnection = (data) => {
  console.log(data)

  // TODO figure out how to ensure everything is a string
  if (!validate(data)) {
    return false
  }

  const params = {
    TableName: 'Connection',
    Item: {
      'id': data.id.toString(),
      'userId': data.userId.toString(),
      'clothingId': data.clothingId.toString(),
      'size': data.size,
      'cost': data.cost,
      'timeObtained': data.timeObtained,
      'fit': data.fit,
    }
  }

  docClient.put(params, function(err, data) {
    if (err) {
      console.error('Unable to add user. Error JSON:', JSON.stringify(err, null, 2))
      return false
    }
    else {
      console.log('PutItem succeeded:', data.id)
      return true
    }
  })
}

//TODO: figure out a general way to ensure type correctness of inputs
const validate = (data) => {
  if (isEmpty(data.id)) return false
  if (isEmpty(data.userId)) return false
  if (isEmpty(data.clothingId)) return false
  if (isEmpty(data.size)) return false
  if (isEmpty(data.cost)) return false
  if (isEmpty(data.timeObtained)) return false
  if (isEmpty(data.fit)) return false

  return true
}

module.exports = router;

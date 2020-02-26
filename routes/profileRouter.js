require('dotenv').config()
const AWS = require('aws-sdk')
const uuidv4 = require('uuid/v4');
const { Router } = require('express')

AWS.config.update({
  region: 'us-west-2',
  endpoint: process.env.DB_ENDPOINT,
})

const docClient = new AWS.DynamoDB.DocumentClient()

const profileRouter = Router()

// get all profiles
profileRouter.get('/profiles', (req, res) => {
  const params = {
    TableName: 'Profiles',
    ProjectionExpression: '#id, #name, #size, #apparel1, #apparel2, #apparel3',
    ExpressionAttributeNames: {
      '#id': 'id',
      '#name': 'name',
      '#size': 'size',
      '#apparel1': 'apparel1',
      '#apparel2': 'apparel2',
      '#apparel3': 'apparel3',
    }
  }

  console.log('[NOTE] Scanning Profile table')
  docClient.scan(params, onScan)

  function onScan(err, data) {
    if (err) {
      console.error('Unable to scan the table. Error JSON:', JSON.stringify(err, null, 2))
    } else {
      res.send(data)

      // log the queried elements
      console.log('[NOTE] Scan succeeded');
      data.Items.forEach((profile) => console.log(profile.id, profile.name, profile.size))

      if (typeof data.LastEvaluatedKey != 'undefined') {
        console.log('[NOTE] Scanning for more...')
        params.ExclusiveStartKey = data.LastEvaluatedKey
        docClient.scan(params, onScan)
      }
    }
  }
})

// create a profile
profileRouter.post('/profiles', (req, res) => {
  console.log(req.body)
  const params = {
    TableName: 'Profiles',
    Item: {
      'id': uuidv4(),
      'name': req.body.name,
      'size': req.body.size,
      'apparel1': req.body.apparel1,
      'apparel2': req.body.apparel2,
      'apparel3': req.body.apparel3,
    }
  }

  docClient.put(params, function(err, data) {
    if (err) {
      console.error('Unable to add profile. Error JSON:', JSON.stringify(err, null, 2))
      res.status(500).send('Unable to add profile')
    }
    else {
      console.log('PutItem succeeded:', req.body.name)
      res.send('OK')
    }
  })
})

// create other routes below

module.exports = profileRouter

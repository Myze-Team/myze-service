require('dotenv').config()
const AWS = require('aws-sdk')
const uuidv4 = require('uuid/v4');
const router = require('express').Router()

AWS.config.update({
  region: 'us-west-2',
  endpoint: process.env.DB_ENDPOINT,
})

const docClient = new AWS.DynamoDB.DocumentClient()

// new user form (GET)
router.get('/', (req, res) => {
  const params = {
    TableName: 'User',
    ProjectionExpression: '#id, #name',
    ExpressionAttributeNames: {
      '#id': 'id',
      '#name': 'name',
    }
  }

  console.log('[NOTE] Scanning User table')
  docClient.scan(params, onScan)

  function onScan(err, data) {
    if (err) {
      console.error('Unable to scan the table. Error JSON:', JSON.stringify(err, null, 2))
    } else {
      res.send(data)

      // log the queried elements
      console.log('[NOTE] Scan succeeded');
      data.Items.forEach((user) => console.log(user.id, user.name))

      if (typeof data.LastEvaluatedKey != 'undefined') {
        console.log('[NOTE] Scanning for more...')
        params.ExclusiveStartKey = data.LastEvaluatedKey
        docClient.scan(params, onScan)
      }
    }
  }
})

// create user (POST)
// expects body to contain the following fields
// NOTE: emails should not be used as user identifiers as not
// all users may have created their accounts with emails
//
// id: <unique id>
// password: <password>
// passwordConfirm: <password>
//
router.post('/new', (req, res) => {
  console.log(req.body)
  const params = {
    TableName: 'User',
    Item: {
      'id': req.body.id.toString(),
      'name': req.body.name,
    }
  }

  docClient.put(params, function(err, data) {
    if (err) {
      console.error('Unable to add user. Error JSON:', JSON.stringify(err, null, 2))
      res.status(500).send('Unable to add user')
    }
    else {
      console.log('PutItem succeeded:', req.body.name)
      res.send('OK')
    }
  })
})

module.exports = router;

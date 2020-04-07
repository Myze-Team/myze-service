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

router.get('/', (req, res) => {
  const params = {
    TableName: 'Clothing',
    ProjectionExpression: '#id, #brand, #type, #name',
    ExpressionAttributeNames: {
      '#id': 'id',
      '#brand': 'brand',
      '#type': 'type',
      '#name': 'name',
    }
  }

  console.log('[NOTE] Scanning Clothing table')
  docClient.scan(params, onScan)

  function onScan(err, data) {
    if (err) {
      console.error('Unable to scan the table. Error JSON:', JSON.stringify(err, null, 2))
    } else {
      res.send(data)

      // log the queried elements
      console.log('[NOTE] Scan succeeded');
      data.Items.forEach((clothing) => console.log(clothing.id, clothing.brand, clothing.type, clothing.name))

      if (typeof data.LastEvaluatedKey != 'undefined') {
        console.log('[NOTE] Scanning for more...')
        params.ExclusiveStartKey = data.LastEvaluatedKey
        docClient.scan(params, onScan)
      }
    }
  }
})

router.post('/new', (req, res) => {
  console.log(req.body)
  if (!validate(req.body)) {
    res.status(400).send('Bad arguments')
    return
  }

  const params = {
    TableName: 'Clothing',
    Item: {
      'id': req.body.id.toString(),
      'brand': req.body.brand,
      'type': req.body.type,
      'name': req.body.name,
    }
  }

  docClient.put(params, function(err, data) {
    if (err) {
      console.error('Unable to add user. Error JSON:', JSON.stringify(err, null, 2))
      res.status(500).send('Unable to add clothing')
    }
    else {
      console.log('PutItem succeeded:', req.body.name)
      res.send('OK')
    }
  })
})

//TODO: figure out a general way to ensure type correctness of inputs
const validate = (data) => {
  if (isEmpty(data.id)) return false
  if (isEmpty(data.brand)) return false
  if (isEmpty(data.type)) return false
  if (isEmpty(data.name)) return false

  return true
}

module.exports = router;

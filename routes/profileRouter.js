require('dotenv').config()
const AWS = require('aws-sdk')
const { Router } = require('express')

AWS.config.update({
  region: 'us-west-2',
  endpoint: process.env.DB_ENDPOINT,
})

const docClient = new AWS.DynamoDB.DocumentClient()

const profileRouter = Router()

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

// create other routes below

module.exports = profileRouter

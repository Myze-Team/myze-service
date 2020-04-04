require('dotenv').config()
const AWS = require('aws-sdk')

AWS.config.update({
  region: 'us-west-2',
  endpoint: process.env.DB_ENDPOINT,
})

const docClient = new AWS.DynamoDB.DocumentClient()

const table = 'User'
const email = 'johnny@gmail.com'

const params = {
  TableName: table,
  Key: { 'email': "" + email }
}

docClient.get(params, (err, data) => {
  if (err)
    console.error('Unable to read item. Error JSON:', JSON.stringify(err, null, 2))
  else
    console.log('GetItem succeeded:', JSON.stringify(data, null, 2))
})

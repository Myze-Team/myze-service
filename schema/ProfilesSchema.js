// defines the schema for the Profiles table
// DynamoDB does not strictly enforce schema conformity
require('dotenv').config()
const AWS = require('aws-sdk')

AWS.config.update({
  region: 'us-west-2',
  endpoint: process.env.DB_ENDPOINT,
})

const dynamodb = new AWS.DynamoDB()

const params = {
  TableName : 'Profiles',
  KeySchema: [{ AttributeName: 'id', KeyType: 'HASH' }],
  AttributeDefinitions: [{ AttributeName: 'id', AttributeType: 'S' }],
  ProvisionedThroughput: {
    ReadCapacityUnits: 5,
    WriteCapacityUnits: 5
  }
}

dynamodb.createTable(params, (err, data) => {
  if (err)
    console.error('Unable to create table. Error JSON:', JSON.stringify(err, null, 2))
  else
    console.log('Created table. Table description JSON:', JSON.stringify(data, null, 2))
})

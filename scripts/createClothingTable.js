require('dotenv').config()
const AWS = require('aws-sdk')
const fs = require('fs')
const uuidv4 = require('uuid/v4');

AWS.config.update({
  region: 'us-west-2',
  endpoint: process.env.DB_ENDPOINT,
})

const dynamodb = new AWS.DynamoDB()
const docClient = new AWS.DynamoDB.DocumentClient()

console.log('END ' + process.env.DB_ENDPOINT)
const params = {
  TableName : 'Clothing',
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
  else {
    console.log('Created table. Table description JSON:', JSON.stringify(data, null, 2))
    console.log('[NOTE] Importing clothing into DynamoDB.')

    const users = JSON.parse(fs.readFileSync('./scripts/clothingData.json', 'utf8'))

    users.forEach((clothing) => {
      const params = {
        TableName: 'Clothing',
        Item: {
          'id': clothing.id,
          'brand': clothing.brand,
          'type': clothing.type,
          'name': clothing.name,
        }
      }

      docClient.put(params, function(err, data) {
        if (err)
          console.error('Unable to add user', clothing.name, '. Error JSON:', JSON.stringify(err, null, 2))
        else
          console.log('PutItem succeeded:', clothing.name)
      })
    })
  }
})

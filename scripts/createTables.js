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

// create User, Clothing, and Connection tables
const createTables = async () => {
  const params = {
    TableName : 'Profile',
    KeySchema: [
      { AttributeName: 'PK', KeyType: 'HASH' },
      { AttributeName: 'SK', KeyType: 'RANGE' },
    ],
    AttributeDefinitions: [
      { AttributeName: 'PK', AttributeType: 'S' },
      { AttributeName: 'SK', AttributeType: 'S' },
      { AttributeName: 'User_GSI', AttributeType: 'S' },
      { AttributeName: 'Acc_GSI', AttributeType: 'S' },
    ],
    GlobalSecondaryIndexes: [
      {
        IndexName: 'User_GSI',
        KeySchema: [
          { AttributeName: 'User_GSI', KeyType: 'HASH' },
          { AttributeName: 'SK', KeyType: 'RANGE' },
        ],
        Projection: {
          ProjectionType: 'ALL',
        },
        ProvisionedThroughput: {
          ReadCapacityUnits: 10,
          WriteCapacityUnits: 10,
        }
      },
      {
        IndexName: 'Acc_GSI',
        KeySchema: [
          { AttributeName: 'Acc_GSI', KeyType: 'HASH' },
          { AttributeName: 'SK', KeyType: 'RANGE' },
        ],
        Projection: {
          NonKeyAttributes: [ 'PK' ],
          ProjectionType: 'INCLUDE',
        },
        ProvisionedThroughput: {
          ReadCapacityUnits: 10,
          WriteCapacityUnits: 10,
        }
      },
    ],
    ProvisionedThroughput: {
      ReadCapacityUnits: 10,
      WriteCapacityUnits:10,
    }
  }

  dynamodb.createTable(params, (err, res) => {
    if (err)
      console.error('Unable to create table. Error JSON:', JSON.stringify(err, null, 2))
    else {
      console.log('Created table. Table description JSON:', JSON.stringify(res, null, 2))
      console.log('[NOTE] Importing data into DynamoDB.')

      const data = JSON.parse(fs.readFileSync('./scripts/tableData.json', 'utf8'))

      data.forEach((item) => {
        const params = {
          TableName: 'Profile',
          Item: item,
        }

        docClient.put(params, function(err, data) {
          if (err)
            console.error('Unable to add item', item.PK, '. Error JSON:', JSON.stringify(err, null, 2))
          else
            console.log('PutItem succeeded:', item.PK)
        })
      })
    }
  })
}

createTables()

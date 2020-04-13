require('dotenv').config()
const AWS = require('aws-sdk')
const fs = require('fs')
const uuidv4 = require('uuid/v4');

AWS.config.update({
  region: 'us-west-2',
  endpoint: process.env.DB_ENDPOINT,
})

const dynamodb = new AWS.DynamoDB()

// deleta pre-existing tables
const deleteTables = async () => {
  const res = await dynamodb.listTables({}).promise()
  //console.log(err, err.stack)
  console.log(res)

  await res.TableNames.forEach(async (table) => {
    var del = await dynamodb.deleteTable({ TableName: table }).promise()
    console.log(del)
  })

  console.log('Finished deleting tables')
}

deleteTables()

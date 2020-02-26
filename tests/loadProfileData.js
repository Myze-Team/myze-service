require('dotenv').config()
const AWS = require('aws-sdk')
const fs = require('fs')

AWS.config.update({
  region: 'us-west-2',
  endpoint: process.env.DB_ENDPOINT,
})

const docClient = new AWS.DynamoDB.DocumentClient()

console.log('[NOTE] Importing profiles into DynamoDB.')
const profiles = JSON.parse(fs.readFileSync('./profileData.json', 'utf8'))

profiles.forEach((profile) => {
  const params = {
    TableName: 'Profiles',
    Item: {
      'id': profile.id,
      'name': profile.name,
      'size': profile.size,
      'apparel1': profile.apparel1,
      'apparel2': profile.apparel2,
      'apparel3': profile.apparel3,
    }
  }

  docClient.put(params, function(err, data) {
    if (err)
      console.error('Unable to add profile', profile.name, '. Error JSON:', JSON.stringify(err, null, 2))
    else
      console.log('PutItem succeeded:', profile.name)
  })
})

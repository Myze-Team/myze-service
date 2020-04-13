require('dotenv').config()
const AWS = require('aws-sdk')
const router = require('express').Router()
const isEmpty = require('is-empty')
const uuid = require('uuid/v4')
const helper = require('./helper')()

AWS.config.update({
  region: 'us-west-2',
  endpoint: process.env.DB_ENDPOINT,
})

const docClient = new AWS.DynamoDB.DocumentClient()

// [GET]: grabs the meta item for a given user
// does not include connection or clothes items
router.get('/:id', (req, res) => {
  helper.getItem(docClient, res, req.params.id)
})

// [GET]: retrieves user id given the accoutn id
router.get('/acc/:acc_id', (req, res) => {
  console.log(req.params)
  const params = {
    TableName: 'Profile',
    IndexName: 'Acc_GSI',
    KeyConditionExpression: 'Acc_GSI = :acc_gsi AND SK = :sk',
    ExpressionAttributeValues: {
      ':acc_gsi': req.params.acc_id,
      ':sk': 'meta',
    }
  }

  console.log('[NOTE] Getting Profile table')
  docClient.query(params, onQuery)

  function onQuery(err, user) {
    if (err) {
      console.error('Unable to query the table. Error JSON:', JSON.stringify(err, null, 2))
      res.status(500).send('Unable to get account')
    } else {
      // item not found
      if (Object.keys(user).length === 0) {
        console.error('User not found:', req.params.id)
        res.status(400).send('Account not found')
        return
      }

      res.send(user.Items[0])

      // log the queried elements
      console.log('[NOTE] Get succeeded')
      console.log(user.PK)
    }
  }
})

// [GET]: grabs all data associated with user
// includes related clothing items
router.get('/:id/clothes', (req, res) => {
  console.log(req.params)
  const params = {
    TableName: 'Profile',
    IndexName: 'User_GSI',
    KeyConditionExpression: 'User_GSI = :user_gsi AND begins_with(SK, :sk)',
    ExpressionAttributeValues: {
      ':user_gsi': req.params.id,
      ':sk': 'conn',
    }
  }

  helper.queryItems(docClient, res, params);
})

// [POST]: create new user
// expects body to contain the following fields
// NOTE: emails should not be used as user identifiers as not
// all users may have created their accounts with emails
//
// id: user id
// name: name of user
//
// NOTE: using an existing id will overwrite the previous item
router.post('/new', (req, res) => {
  // validate parameters
  if (!validate(req.body)) {
    res.status(400).send('Bad arguments')
    return
  }

  const params = {
    TableName: 'Profile',
    Item: {
      'PK': 'user_'.concat(uuid()),
      'SK': 'meta',
      'Acc_GSI': req.body.acc_id.toString(),
      'name': req.body.name.toString(),
    }
  }

  helper.putItem(docClient, res, params)
})

const validate = (data) => {
  if (isEmpty(data.acc_id)) return false
  if (isEmpty(data.name)) return false

  return true
}

module.exports = router;

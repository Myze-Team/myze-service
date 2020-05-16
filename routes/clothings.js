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

// [GET]: grabs the meta item for a given clothing
// does not include connection or user items
router.get('/:id', (req, res) => {
  // TODO: verify that the id begins with 'clothes_'
  helper.getItem(docClient, res, req.params.id)
})

// [GET]: grabs all data associated with clothes
// includes related user items
router.get('/:id/users', (req, res) => {
  const params = {
    TableName: 'Profile',
    KeyConditionExpression: 'PK = :pk AND begins_with(SK, :sk)',
    ExpressionAttributeValues: {
      ':pk': req.params.id,
      ':sk': 'conn',
    }
  }

  helper.queryItems(docClient, res, params);
})

// [POST]: create new clothing
// expects body to contain the following fields:
//
// name: <name of clothing>
// brand: <brand/company>
// type: <style of clothing>
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
      'PK': 'clothes_'.concat(uuid()),
      'SK': 'meta',
      'name': req.body.name.toString(),
      'brand': req.body.brand.toString(),
      'type': req.body.type.toString(),
    }
  }

  helper.putItem(docClient, res, params)
})

//TODO: figure out a general way to ensure type correctness of inputs
const validate = (data) => {
  if (isEmpty(data.name)) return false
  if (isEmpty(data.brand)) return false
  if (isEmpty(data.type)) return false

  return true
}

module.exports = router;

module.exports = () => {
  function getItem(docClient, res, pk) {
    const params = {
      TableName: 'Profile',
      Key: {
        'PK': pk,
        'SK': 'meta',
      }
    }

    docClient.get(params, (err, data) => {
      if (err) {
        console.error('Unable to get item. Error JSON:', JSON.stringify(err, null, 2))
        res.status(500).send('Unable to get item')
      }
      else {
        if (Object.keys(data).length === 0) {
          console.error('Item not found:', pk)
          res.status(400).send('Item not found')
          return
        }

        console.log('[NOTE] getItem succeeded');
        console.log(data)
        res.send(data.Item)
      }
    })
  }

  function queryItems(docClient, res, params) {

    console.log('[NOTE] Querying Profile table')
    docClient.query(params, onQuery)

    function onQuery(err, data) {
      if (err) {
        console.error('Unable to query the table. Error JSON:', JSON.stringify(err, null, 2))
        res.status(500).send('Unable to query items')
      } else {
        res.send(data.Items)

        console.log('[NOTE] Query succeeded')
        data.Items.forEach((item) => console.log(item.PK, item.SK))

        // go for a second round if there's more
        if (typeof data.LastEvaluatedKey != 'undefined') {
          console.log('[NOTE] Querying for more...')
          params.ExclusiveStartKey = data.LastEvaluatedKey
          docClient.scan(params, onQuery)
        }
      }
    }
  }

  function putItem(docClient, res, params) {
    docClient.put(params, function(err, data) {
      if (err) {
        console.error('Unable to put item. Error JSON:', JSON.stringify(err, null, 2))
        res.status(500).send('Unable to put item')
      }
      else {
        console.log('PutItem succeeded')
        console.log(params.Item.PK)
        res.send({ 'id': params.Item.PK })
      }
    })
  }

  return {
    getItem,
    queryItems,
    putItem,
  }
}

const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const server = require('http').createServer(app)

const profileRouter = require('./routes/profileRouter')

// json body parser
app.use(express.json())

// add routes
app.use(profileRouter)

/*
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
*/


// TODO: test to be removed
app.get('/', async(req, res, next) => {
  res.send('Hello, world')
})

const port = process.env.PORT || 3000
server.listen(port, () => {
  console.log(`server listening on port ${port}`)
})

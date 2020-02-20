const express = require('express')
const app = express()
const server = require('http').createServer(app)

const profileRouter = require('./routes/profileRouter')

app.use(profileRouter)

app.get('/', async(req, res, next) => {
  res.send('Hello, world')
})

const port = process.env.PORT || 3000
server.listen(port, () => {
  console.log(`server listening on port ${port}`)
})

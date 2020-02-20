const { Router } = require('express')

const profileRouter = Router()

profileRouter.get('/profiles', (req, res) => {
  // TODO
  res.send('profiles')
})

// create other routes below

module.exports = profileRouter

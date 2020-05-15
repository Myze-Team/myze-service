const express = require('express')
const app = express()


//
// ---- MIDDLEWARE
//


// json body parser
app.use(express.json())


//
// ---- ROUTES
//

// serve static files
//app.use(express.static(path.join(__dirname, '/public')))

app.get('/', (req, res) => {
  res.send('Hello, world!')
})

app.use('/users', require('./firebase/authenticate'))
app.use('/users', require('./routes/users'))
app.use('/clothings', require('./firebase/authenticate'))
app.use('/clothings', require('./routes/clothings'))

// test routes
app.use('/testauth', require('./firebase/authenticate'))
app.get('/testauth', (req, res) => {
  res.status(200).send({
    auth: true,
    message: 'Authenticated user. You are currently logged in as ' + res.locals.userInfo.uid,
  })
})


// export the express app with the attatched middleware
// and routes
//
// import the app where needed to create server instances
module.exports = app

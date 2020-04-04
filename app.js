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
  res.render('landing')
})
app.use('/users', require('./routes/users'))

// test routes
app.use('/testauth', require('./firebase/authenticate'))
app.get('/testauth', (req, res) => {
  res.status(200).send({
    auth: true,
    message: 'Authenticated user. You are currently logged in as ' + res.locals.uid,
  })
})


// export the express app with the attatched middleware
// and routes
//
// import the app where needed to create server instances
module.exports = app

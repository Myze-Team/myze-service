require('dotenv').config()
const app = require('./app')


// choose a port to listen on
const port = process.env.PORT || 3000

// begin listening
app.listen(port, () => {
  console.log('App is listening on port ' + port)
})

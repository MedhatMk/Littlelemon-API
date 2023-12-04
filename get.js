const axios = require('axios')

// axios.get("http://127.0.0.1:8000/api/menu-items")
// .then(res => console.log(res.data.results));

axios.get('http://127.0.0.1:8000/api/menu-items')
  .then(function (response) {
    // handle success
    console.log(response.data.results);
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
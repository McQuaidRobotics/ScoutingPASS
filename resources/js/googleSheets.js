function setUpGoogleSheets() {
    const scriptURL = 'https://script.google.com/macros/s/AKfycbzrsuEjN8QiJXGEDb6de3C2XzHW0NGgsMd3QCpJqtWH7UYmg8rjl6Q-yXThOH61h-uX/exec'
    const form = document.querySelector('#scoutingForm')
    const btn = document.querySelector('#submit')
 
    
    form.addEventListener('submit', e => {
      e.preventDefault()
      btn.disabled = true
      btn.innerHTML = "Sending..."

      let fd = getData(false)
      // for (const [key, value] of fd) {
      //   console.log(`${key}: ${value}\n`);
      // }

      console.log(fd);
      fetch(scriptURL, { method: 'POST', mode: 'no-cors', body: fd })
        .then(response => { 
              console.log(response); })
        .catch(error => {
              alert('Error!'); console.log(error);})

      btn.disabled = false
      btn.innerHTML = "Send to Google Sheets"
    })
}

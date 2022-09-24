var change_buttons = document.querySelectorAll('.change');

change_buttons.forEach((e) => {
    e.onclick = function() {
         const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            data = {'status': e.dataset.status,'app_id': e.dataset.appid,};
            fetch('http://127.0.0.1:8000/status_data/',   {
                   method: 'POST',
                   body: JSON.stringify(data),
                   headers: {
                            'X-CSRFToken': csrftoken,
                            'Accept': 'text/html',
                            'Content-Type': 'application/json',
                        }})
                   .then(response => response.text())
                   .then(temp => {
                       console.log(temp)
                       div_mes = document.querySelector('.icons_approve')
                       var status = document.createElement('h3')
                       status.innerHTML = temp
                       div_mes.innerHTML = '';
                       div_mes.appendChild(status)
                       })
                   .catch(error => console.log(error))
                    console.log(e.dataset.status)
    }
});



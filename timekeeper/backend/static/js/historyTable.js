csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value

function onChangeSelect(isMonth, year, number){
  window.location.href = `${window.location.pathname}?month=${isMonth}&year=${year}&number=${number}`;
}

function editInput(elementId) {
  targetElement = document.getElementById(elementId)
  targetElement.disabled = !targetElement.disabled
}

function deleteRecord(elementId) {
  fetch(`/delete_record/${elementId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
  })
  .then(result => {
    window.location.reload()
  })
  .catch(error => {
    console.error(error)
  })
}
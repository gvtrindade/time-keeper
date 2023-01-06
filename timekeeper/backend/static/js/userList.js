csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value

function deleteUser(userId) {
  fetch(`/delete_user/${userId}`, {
    method: 'POST',
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
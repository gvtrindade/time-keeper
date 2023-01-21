csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value

let dataType, dataId;

function showConfirmModal(type, title, id) {
  const deletedDataType = document.getElementById('deletedDataType')
  const deletedDataTitle = document.getElementById('deletedDataTitle')
  deletedDataType.innerHTML = type
  deletedDataTitle.innerHTML = title
  dataType = type
  dataId = id
}

function handleDelete() {
  switch (dataType) {
    case 'user':
      deleteUser(dataId)
      break;
    case 'record':
      deleteRecord(dataId)
      break;

    default:
      break;
  }
}

function deleteUser(userId) {
  fetch(`auths/delete_user/${userId}`, {
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
    .finally(result => {
      dataType = ''
      dataId = -1
    })
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
    .finally(result => {
      dataType = ''
      dataId = -1
    })
}
csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value

let dataType, dataId;

function showDeleteConfirmModal(type, title, id) {
  const confirmModalTitle = document.getElementById('confirmModalTitle')
  const modalContent = document.getElementById('delete-modal-content')
  const deletedDataType = document.getElementById('deletedDataType')
  const deletedDataTitle = document.getElementById('deletedDataTitle')
  confirmModalTitle.innerHTML = 'Delete'
  modalContent.hidden = false
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

function showRegisterConfirmModal() {
  const confirmModalTitle = document.getElementById('confirmModalTitle')
  const modalContent = document.getElementById('register-modal-content')
  confirmModalTitle.innerHTML = 'Clock-out'
  modalContent.hidden = false
}

function handleRegister() {
  const breakDuration = document.getElementById('breakDuration').value
  let formData = new FormData()
  formData.append('action', 'Clock-out')
  formData.append('breakDuration', breakDuration)

  registerRecord(formData);
}

function registerRecord(formData) {
  fetch(window.location.href, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    body: formData
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

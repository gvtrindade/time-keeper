csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value

function onChangeSelect(isMonth, year, number) {
  window.location.href = `${window.location.pathname}?month=${isMonth}&year=${year}&number=${number}`;
}

function editInput(elementId) {
  targetElement = document.getElementById(elementId)
  targetElement.disabled = !targetElement.disabled
}

function showRemarks(recordId) {
  const remark = document.getElementById(`remarks${recordId}`)
  remark.hidden = !remark.hidden
}
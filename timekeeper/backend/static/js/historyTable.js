csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
selectYear = document.getElementById('selectYear')
selectMont = document.getElementById('selectMonth')
selectWeek = document.getElementById('selectWeek')

function handleFilter(week) {
  year = selectYear.value
  month = selectMont.value
  window.location.href = `${window.location.pathname}?year=${year}&month=${month}&week=${week}`;
}

function editInput(elementId) {
  targetElement = document.getElementById(elementId)
  targetElement.disabled = !targetElement.disabled
}

function showRemarks(recordId) {
  const remark = document.getElementById(`remarks${recordId}`)
  remark.hidden = !remark.hidden
}
csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
updateCheckboxes(0)

function updateCheckboxes() {
    const year = document.querySelector('.yearExport').value
    const month = parseInt(document.querySelector('.monthExport').value) - 1
    const checkboxes = document.querySelector('.checkboxes')
    checkboxes.innerHTML = ''
    
    const { firstWeek, lastWeek } = getFirstAndLastWeekNumber(year, month)
    
    for (let i = 0; i < 5; i++) {
        appendCheckbox(i, firstWeek, year, checkboxes)
    }
}

function appendCheckbox(i, firstWeek, year, checkboxes) {
    const currentWeek = firstWeek + i
    const { firstWeekDay, lastWeekDay } = getFirstAndLastWeekDay(year, currentWeek)
    const isLastWeek = getWeekByDate(new Date()) - 1 == currentWeek
    if(i > 3 && isNaN(parseInt(firstWeekDay[1]))) return

    const input = document.createElement('input')
    const label = document.createElement('label')

    input.type = 'checkbox'
    input.id = `week${currentWeek}`
    input.name = `week${currentWeek}`
    input.classList.add('weekCheckbox')
    input.value = currentWeek
    input.style.marginLeft = '0.6em'
    input.style.marginRight = '0.1em'
    input.checked = isLastWeek
    
    label.htmlFor = `week${currentWeek}`
    label.innerText = `${firstWeekDay}-${lastWeekDay}`

    checkboxes.appendChild(input)
    checkboxes.appendChild(label)
}

function getFirstAndLastWeekDay(year, currentWeek) {
    const firstWeekDate = getDateOfWeek(year, currentWeek)
    let lastWeekDate = new Date(firstWeekDate.valueOf())
    lastWeekDate.setDate(lastWeekDate.getDate() + 6)

    const firstWeekDay = ordinal_number(firstWeekDate.getDate())
    const lastWeekDay = ordinal_number(lastWeekDate.getDate())
    return { firstWeekDay, lastWeekDay }
}

function getFirstAndLastWeekNumber(year, month) {
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    
    const firstWeek = getWeekByDate(firstDay) !== 0 ? getWeekByDate(firstDay) : 1
    const lastWeek = getWeekByDate(lastDay)
    
    return { firstWeek, lastWeek }
}

function getDateOfWeek(year, week) {
    const day = (2 + (week - 1) * 7)
    return new Date(year, 0, day)
}

function getWeekByDate(date) {
    const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
    const pastDaysOfYear = (date - firstDayOfYear) / 86400000;
    return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
}

function ordinal_number(number) {
    let suffix;
    switch (number){
        case 1 | 21 | 31:
            suffix = 'st'
        case 2 | 22:
            suffix = 'nd'
        case 3 | 23:
            suffix = 'rd'
        default:
            suffix = 'th'
    }
    return `${number}${suffix}`
}

async function downloadFile() {
    const year = document.querySelector('.yearExport').value
    const month = parseInt(document.querySelector('.monthExport').value) - 1
    const checkboxes = [...document.querySelectorAll('.weekCheckbox:checked')]
    const weeks = checkboxes.map(box => box.value)
    if(weeks.length <= 0) return //TODO show message indicating form validation

    await fetch(`export`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            year: year,
            weeks: weeks
        })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${year} - ${month}.xlsx`
        document.body.appendChild(a)
        a.click()
        a.remove()
    })
    .then(() => {
        $('#exportModal').modal('hide')
    })
    .catch(error => {
        console.error(error)
    })
}

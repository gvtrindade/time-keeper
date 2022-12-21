const timeDiv = document.getElementById('clock');

function getCurrentTime() {
    const date = new Date().toLocaleTimeString('en-US', {timeZone: 'Europe/London'});
    timeDiv.innerText = date;
}

setInterval(getCurrentTime, 1000);
const timeDiv = document.getElementById('clock');

function getCurrentTime() {
    const date = new Date().toLocaleTimeString('en-US');
    timeDiv.innerText = date;
}

setInterval(getCurrentTime, 1000);
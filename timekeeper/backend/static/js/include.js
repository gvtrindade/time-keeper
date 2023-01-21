function hideBreakDuration() {
    const actionSelect = document.getElementById("actionSelect");
    const breakDuration = document.getElementById("breakDuration");
    actionSelect.value == "Clock-out" ? breakDuration.hidden = false : breakDuration.hidden = true
}
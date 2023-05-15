inputs = document.getElementsByClassName('password-input')

if (inputs.length === 0) {
    inputs = document.querySelectorAll('[id^=id_new_password]')
}

Array.from(inputs).forEach(input => {
    input.classList.add('form-control')
    parent = input.parentNode
    parent.classList.add('input-group', 'flex-nowrap', 'my-2')

    label = parent.querySelector('label')
    label.classList.add('input-group-text')

    createShowPasswordButton(input)
})

function createShowPasswordButton(element) {
    const toggleButton = document.createElement('button')
    toggleButton.innerHTML = '<i id="passwordIcon" class="bi bi-eye-slash"></i>'
    toggleButton.classList.add('input-group-text', 'password-button')
    toggleButton.onclick = showPassword

    element.parentNode.appendChild(toggleButton)
}

function showPassword(event) {
    event.preventDefault()

    const parent = event.target.tagName === 'I' ? event.target.parentNode.parentNode : event.target.parentNode
    const input = parent.querySelector('input')
    const icon = parent.querySelector('i')

    if (input.type === 'password') {
        input.type = 'text'
        icon.classList.remove('bi-eye-slash')
        icon.classList.add('bi-eye')
    } else {
        input.type = 'password'
        icon.classList.remove('bi-eye')
        icon.classList.add('bi-eye-slash')
    }
}
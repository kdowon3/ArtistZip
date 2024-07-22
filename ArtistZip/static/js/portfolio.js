function enableEditing(element) {
    element.contentEditable = 'true';
    element.classList.add('editable');
    element.focus();
}

function disableEditing(element) {
    element.contentEditable = 'false';
    element.classList.remove('editable');
    var inputElement = document.getElementById(element.dataset.inputId);
    if (inputElement) {
        inputElement.value = element.innerText.trim();
    }
}

function handleFileSelect(event, previewId) {
    var reader = new FileReader();
    reader.onload = function (event) {
        var img = document.getElementById(previewId).querySelector('img');
        img.setAttribute('src', event.target.result);
        img.style.display = 'block';
        var placeholderText = document.getElementById(previewId).querySelector('.placeholder-text');
        if (placeholderText) {
            placeholderText.style.display = 'none';
        }
    };
    reader.readAsDataURL(event.target.files[0]);
}

function triggerFileInput(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        input.click();
    }
}

function openLink(type) {
    let url;
    switch (type) {
        case 'instagram':
            url = document.getElementById('instagram-input').value;
            break;
        case 'email':
            url = 'mailto:' + document.getElementById('email-input').value;
            break;
        case 'homepage':
            url = document.getElementById('homepage-input').value;
            break;
    }
    if (url) {
        window.open(url, '_blank');
    } else {
        alert('URL이 설정되지 않았습니다.');
    }
}

function saveChanges() {
    document.getElementById('portfolio-form').submit();
}

var API_URL = `${window.location.href.slice(0, -6)}:7000`;
var files_div = document.querySelector("#file-items-div");
var preloader_div = document.querySelector("#preloader");

const notification_component = (title) => {
    let notification = document.querySelector("#notification-1");
    notification.classList.add("notification-item-push");
    notification.innerText = title;
    setTimeout(() => {
        notification.classList.remove("notification-item-push");
    }, 3000);
}

function checkFileSize(selectedFile) {
    const fileSizeInBytes = selectedFile.size;
    const fileSizeInKb = fileSizeInBytes / 1024;
    const fileSizeInMb = fileSizeInKb / 1024;

    alert(`File size: ${fileSizeInBytes} bytes (${fileSizeInKb} KB or ${fileSizeInMb} MB)`);
}


const file_component = (name, size) => {
    return `<div id="${name}" class="bucket-item">
                <div>
                    <abbr title="${name}"><h4>${name.toString().slice(0, 18)}...</h4></abbr>
                    <p>${size}MB</p>
                </div>
                <img id="${name}-downloadimg" onclick="downloadThatFile('${name}')" class="icon" width="25" height="25" src="https://img.icons8.com/windows/96/download--v1.png"
                        alt="download--v1" />
                <?xml version="1.0" encoding="utf-8"?>
                        <svg id="${name}-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto; background: none; display: none; shape-rendering: auto;scale:1.4;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                        <circle cx="50" cy="50" fill="none" stroke="#1d0e0b" stroke-width="1" r="10" stroke-dasharray="47.12388980384689 17.707963267948966">
                          <animateTransform attributeName="transform" type="rotate" repeatCount="indefinite" dur="1s" values="0 50 50;360 50 50" keyTimes="0;1"></animateTransform>
                        </circle>
                        <!-- [ldio] generated by https://loading.io/ --></svg>
                <img onclick="deleteThatFile('${name}')" class="icon" width="30" height="30" src="https://img.icons8.com/ios/100/multiply.png"
                        alt="multiply" />
            </div>`
}

async function getIp() {
    try {
        const response = await fetch(`${API_URL}/get_local_ip`);
        const data = await response.json();

        const ip_span = document.querySelector("#ip-span");
        const qrcodeDiv = document.getElementById("qrcode");

        ip_span.innerText = data.ip + ":7000";

        const qrcode = new QRCode(qrcodeDiv, {
            text: data.ip + ":7000",
            width: 204,
            height: 204
        });

        notification_component("Connection established")
    } catch (error) {
        preloader_div.style.display = 'flex';
        setTimeout(() => { preloader_div.innerText = 'Reloading...' }, 3000)
        setTimeout(() => { window.location.reload(); }, 4000)
        console.error('Error:', error);
    }
}

async function loadFilesFromSharedData() {
    await fetch(`${API_URL}/all-files`)
        .then(response => response.json())
        .then(data => {

            let no_items_message = document.querySelector("#center-message");

            if (data.length == 0) {
                no_items_message.style.display = 'block';
            }

            for (const file of data) {
                files_div.innerHTML += file_component(file.filename, file.size_mb.toString().slice(0, 5))
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}



// DOWNLOADING THE FILE...

function saveBlobAsFile(blob, fileName) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
    document.body.removeChild(a);
}


async function downloadThatFile(filename) {
    notification_component("Downloading...")
    let downloadButton = document.getElementById(`${filename}-downloadimg`);
    let downloadingIcon = document.getElementById(`${filename}-svg`);

    downloadButton.style.display = 'none';
    downloadingIcon.style.display = 'block';
    await fetch(`${API_URL}/file`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: filename }),
        mode: 'cors'
    })
        .then(response => { return response.blob() })
        .then(blob => {
            downloadButton.style.display = 'block';
            downloadingIcon.style.display = 'none';
            notification_component("Download Completed!")
            saveBlobAsFile(blob, filename)
        })
        .catch(error => {
            console.error('Error:', error);
        });

}

async function deleteThatFile(filename) {
    await fetch(`${API_URL}/file`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: filename }),
        mode: 'cors'
    })
        .then(response => { return response.json() })
        .then(data => {
            console.log(data);
            document.getElementById(filename).remove()
            notification_component(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

async function uploadFiles() {
    const fileInput = document.getElementById('file-upload-input');
    const files = fileInput.files;

    if (files.length === 0) {
        notification_component("Please select one or more files.");
        return;
    }

    const progressBar = document.querySelector("#progress-div");
    progressBar.value = 0;

    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        console.log("Uploading file " + files[i].name);
        formData.append('file', files[i]);
    }

    const xhr = new XMLHttpRequest();
    xhr.open('PUT', `${API_URL}/file`, true);

    xhr.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable) {
            const percentComplete = (event.loaded / event.total) * 100;
            const newConicGradientValue = `#d4cbdb ${percentComplete.toString().slice(0, 4)}%, #f8f0ff 0`; // Replace with the desired value
            console.log(newConicGradientValue);
            progressBar.style.background = `radial-gradient(closest-side, rgb(248 240 255) 79%, transparent 80% 100%), conic-gradient(${newConicGradientValue})`;
            progressBar.value = percentComplete;
        }
    });

    xhr.onload = async function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            const response = JSON.parse(xhr.responseText);
            console.log(response);
            showHideUpload()
            notification_component(response.message);
            // await loadFilesFromSharedData();
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            console.error('Error:', xhr.statusText);
        }
    };

    xhr.onerror = function () {
        console.error('Network error');
    };

    xhr.send(formData);
}


window.onload = async () => {
    await getIp();
    await loadFilesFromSharedData();
};
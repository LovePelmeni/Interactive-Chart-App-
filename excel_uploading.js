var redirectURL = new URL('http://127.0.0.1:8000');


function GetUploadedFileDataInfo(file){

    var fileData = new FormData(file);

    var url = new URL('http://127.0.0.1:8000/get/file/datasource/data/');
    var request = new XMLHttpRequest();

    request.open('POST', url, false);
    request.send(fileData);

    console.log(request);

    var session_key = JSON.parse(request.responseText).session_key;
    redirectURL.searchParams.append('session_key', session_key);

    return window.location.replace(redirectURL);
}

FileForm.addEventListener('submit', function(event){
    event.preventDefault();
    return ValidateFileForm();
});

function ValidateFileForm(){

    var file = $('#FileForm')[0];
    var formData = new FormData(file);

    var url = new URL('http://127.0.0.1:8000/validate/file/form/');

    var request = new XMLHttpRequest();
    request.open('POST', url, false);

    request.send(formData);
    data = JSON.parse(request.responseText);

    console.log(data);
    if (data.is_valid == true){

        console.log('form is valid.....');
        return GetUploadedFileDataInfo(file);

    } else {
        console.log('form is not valid.....');
    }
};
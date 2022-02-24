var redirectURL = new URL('http://127.0.0.1:8000');
var validate_url = new URL("http://127.0.0.1:8000/validate/stock/form/");

StockForm.addEventListener('submit', function(event){

    event.preventDefault();
    console.log('started.....');

    var formData = $(this).serialize();
    console.log(formData);

    $.ajax({
        url: validate_url,
        type: 'POST',
        data: formData,

        dataType: 'json',

        success: function(response){

            console.log(formData);
            if (response.is_valid == true){
                console.log('form has been passed through syntax validation....');

                content = {'data_source_url': StockForm.source_url.value, 'slot': StockForm.slot.value}
                var response = GetDataSourceInfo(content);
                RegisterForm.removeClass('is-invalid').addClass('is-valid');

                $('#Error').remove();
            }
            else {
                    $('#StockForm').removeClass('is-valid').addClass('is-invalid');
                    $('#StockForm').after('<div class="invalid-feedback d-block" id="Error">Invalid Data...</div>');

                    $('#Error').remove();
                    console.log('data has been sended....');
                }
            },
        error: function(error){
            console.log('error has occurred', error);
        }
    });

});

function getYesterDayDate(){

        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0') - 1;
        var mm = String(today.getMonth() + 1).padStart(2, '0');
        var yyyy = today.getFullYear();

        today = String(yyyy + '-' + mm + '-' + dd);
        return today;
}

function getCurrentDate(){

        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0');
        var yyyy = today.getFullYear();

        today = String(yyyy + '-' + mm + '-' + dd);
        return today;
}

function GetDataSourceInfo(content_params){

    start_point = getYesterDayDate()
    end_point = getCurrentDate();
    console.log('started.... function......');

    var file_url = new URL('http://127.0.0.1:8000/get/datasource/data/');
    console.log(content_params.slot, content_params.data_source_url);

    file_url.searchParams.append('points', [start_point, end_point]);
    file_url.searchParams.append('data_source_url', content_params.data_source_url);

    file_url.searchParams.append('slot', content_params.slot)

    console.log(file_url);

    var request = new XMLHttpRequest();

    request.open('GET', file_url, false);
    request.setRequestHeader('Accept', 'text/csv');

    console.log(request);
    request.send(null);

    var session_key = JSON.parse(request.responseText).session_key;
    redirectURL.searchParams.append('session_key', session_key);

    return window.location.replace(redirectURL);
}

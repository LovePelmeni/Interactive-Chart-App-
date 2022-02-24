// need to catch data from redirect and then put it in a csv decoder.....


console.log('started....');
console.log(window.location.href);

var current_url = new URL(window.location.href);
var ChartNamesList = {'PolarAreaChart': 'polarArea', 'LineChart' :'line', 'BarChart' :'bar', 'RadarChart' :'radar'}

if (!current_url.searchParams.get('session_key')){
    console.log('session key is not specified....');
    label = 'Not Selected';
//    Banner.innerHTML = 'Default Table';

    keys = [];
    values = [];
    setChart(label, keys, values);

} else {
//Banner.innerHTML = 'Your Table';

var req_url = new URL('http://127.0.0.1:8000/get/session/data/');
req_url.searchParams.append('session_key', current_url.searchParams.get('session_key'));

var request = new XMLHttpRequest();
request.open('GET', req_url, false);

request.setRequestHeader('Accept', 'text/csv');
request.send(null);

console.log(request);
var decoded_data = CSVToJSON(request.responseText);

    try {
        var parsedCSVData = CSVToJSON(request.responseText);
        console.log(parsedCSVData);

        var keys = Object.keys(parsedCSVData[0]);
        var values = Object.values(parsedCSVData[0]);

        var label = 'My Table';
        setChart(label, keys, values);

    } catch (CSVDataError){
        alert('Seems like data has been encoded incorrectly :( Decode Error!');
        console.log('data cannot be decoded.....');
    }
}

function CSVToJSON(csv){

    decodedList = []
    data = $.csv.toArray(csv)
    console.log(data);

    data.forEach(function(index, item){
        console.log(index, item);

        dec_item = eval('(' + index.slice(1) + ')');
        console.log(dec_item);

        decodedList.push(dec_item);
    });
    console.log(decodedList);
    return decodedList
}

function setChart(label, keys, values){

    for (var chart_name in ChartNamesList){

        var myChart = new Chart(chart_name, {
        type: ChartNamesList[chart_name],
        data: {
            labels: keys, // list of dataframe columns.....
            datasets: [{
                label: label,
                data: values, // so this is last values of columns.... Gonna find out more about it...
                backgroundColor: [

                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)', // also need to specify quantity of colors as much as labels quantity
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'

                ],

            borderColor: [

                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)', // same thing as
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'

            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
}}


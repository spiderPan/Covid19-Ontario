jQuery(function($) {
    feather.replace()

    // Graphs
    var ctx = $('#myChart'),
        ontario_data = ctx.data('status'),
        dates = [],
        confirmed_cases = [],
        resolved_cases = [],
        deceased_cases = [];

    ontario_data.forEach(function(daily) {
        dates.push(daily['date']);
        confirmed_cases.push(daily['confirmed']['total']);
        resolved_cases.push(daily['resolved']);
        deceased_cases.push(daily['deceased']);
    });
    // eslint-disable-next-line no-unused-vars
    var myChart = new Chart(ctx.get(), {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                    data: confirmed_cases,
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: '#dc3545',
                    borderWidth: 4,
                    pointBackgroundColor: '#dc3545'
                }, {
                    data: resolved_cases,
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: '#28a745',
                    borderWidth: 4,
                    pointBackgroundColor: '#28a745'
                },
                {
                    data: deceased_cases,
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: '#343a40',
                    borderWidth: 4,
                    pointBackgroundColor: '#343a40'
                }
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
            },
            legend: {
                display: false
            }
        }
    });
});
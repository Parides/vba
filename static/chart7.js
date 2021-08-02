let colors4 = ['rgba(255, 99, 132, 0.4)', 'rgba(54, 162, 235, 0.4)', 'rgba(255, 206, 86, 0.4)', 'rgba(75, 192, 192, 0.4)', 'rgba(153, 102, 255, 0.4)'];
let bcolors4 = ['rgba(255,99,132,1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)'];
// define the chart data
var chartData = {
    labels : [{% for item in labels %}
                "{{item}}",
                {% endfor %}],
    datasets : [{
        data : [{% for item in datasets %}
                    {{item}},
                {% endfor %}],

        backgroundColor: colors4,
        borderColor: bcolors4,
        borderWidth: 1
    }]
}

var options = {
    title: {
        text: "Attendance percentage per module (%)",
        display: true
    },
    scales: {
        yAxes: [{
            display: true,
            ticks: {
                suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                // beginAtZero: true   // minimum value will be 0.
            }
        }]
    },
    legend: {
        display: false
    },
        tooltips: {
        enabled: true
    },

    animation: {
        duration: 2000, //ms
        easing: 'easeInOutQuint'
    }

}

// get chart canvas
var ctx = document.getElementById("myChart23").getContext("2d");

// create the chart using the chart canvas
var myChart = new Chart(ctx, {
type: 'bar',
data: chartData,
options: options
});
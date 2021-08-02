let labels4 = ['Module 1', 'Module 2', 'Module 3', 'Module 4', 'Module 5'];
let data4 = [73, 67, 66, 61, 90, 80];
// let colors4 = ['#49A9EA', '#36CAAB', '#34495E', '#B370CF', '#AC5353'];
let colors4 = ['rgba(255, 99, 132, 0.4)', 'rgba(54, 162, 235, 0.4)', 'rgba(255, 206, 86, 0.4)', 'rgba(75, 192, 192, 0.4)', 'rgba(153, 102, 255, 0.4)'];
let bcolors4 = ['rgba(255,99,132,1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)'];

let myChart4 = document.getElementById("myChart4").getContext('2d');

let chart4 = new Chart(myChart4, {
    type: 'bar',
    data: {
        labels: labels4,
        datasets: [ {
            data: data4,
            backgroundColor: colors4,
            borderColor: bcolors4,
            borderWidth: 1
        }],
    },
    options: {
        title: {
            text: "Attendance percentage per module (%)",
            display: true
        },
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                    suggestedMax: 100,
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
});
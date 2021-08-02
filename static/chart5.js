var myChart = new Chart(myChart5, {
    type: 'bar',
    data: {
        labels: ["Session 1", "Session 2", "Session 3", "Session 4", "Session 5", "Session 6", "Session 7", "Session 8", "Session 9", "Session 10"],
        datasets: [{
            label: "Attendance Per Session",
            backgroundColor: ['rgba(255, 99, 132, 0.4)', 'rgba(54, 162, 235, 0.4)', 'rgba(255, 206, 86, 0.4)', 'rgba(75, 192, 192, 0.4)', 'rgba(153, 102, 255, 0.4)', 'rgba(255, 99, 132, 0.4)', 'rgba(54, 162, 235, 0.4)', 'rgba(255, 206, 86, 0.4)', 'rgba(75, 192, 192, 0.4)', 'rgba(153, 102, 255, 0.4)'],
            borderColor: ['rgba(255,99,132,1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255,99,132,1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)'],
            data: [0.10, 0.80, 0.80, 0.10, 0.90,0.30, 0.90,0.30, 0.60, 0.60,],
            borderWidth: 1
        }]
    },
    options: {

        responsive: true,
        
        title: {
            text: "Attendance percentage per session (%)",
            display: true
        },
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                    suggestedMax: 1,
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
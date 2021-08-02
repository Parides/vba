var myChart = new Chart(myChart6, {
    type: 'doughnut',
    data: {
      labels: ["Attended", "Misse"],
      datasets: [{
        label: "Attendance(%)",   
        backgroundColor: ['rgba(255, 99, 132, 0.4)', 'rgba(54, 162, 235, 0.4)'],
        borderColor: ['rgba(255,99,132,1)', 'rgba(54, 162, 235, 1)'],
        data: [90, 10]
      }]
    },
    options: {

      responsive: true, 

      title: {
        display: false,
        text: 'Predicted world population (millions) in 2050'
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
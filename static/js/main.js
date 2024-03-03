function showOffcanvas() {
    let offcanvasElement = document.getElementById("offcanvasExample");
    let offcanvas = new bootstrap.Offcanvas(offcanvasElement);
    offcanvas.show();
}

const ctx = document.getElementById("myChart");
const ctx1 = document.getElementById("myChart1");
const ctx2 = document.getElementById("myChart2");
const ctx3 = document.getElementById("myChart3");
const ctx4 = document.getElementById("myChart4");

// Expenses Bar Chart
new Chart(ctx, {
    type: "bar",
    data: {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        datasets: [
            {
                label: "# of Votes",
                data: [12, 19, 3, 5, 2, 3],
                borderWidth: 1,
            },
        ],
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
            },
        },
    },
});

// Income Bar Chart
new Chart(ctx1, {
  type: "bar",
  data: {
      labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
      datasets: [
          {
              label: "# of Votes",
              data: [12, 19, 3, 5, 2, 3],
              borderWidth: 1,
          },
      ],
  },
  options: {
      scales: {
          y: {
              beginAtZero: true,
          },
      },
  },
});

// Budget Bar Chart
new Chart(ctx2, {
  type: "bar",
  data: {
      labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
      datasets: [
          {
              label: "# of Votes",
              data: [12, 19, 3, 5, 2, 3],
              borderWidth: 1,
          },
      ],
  },
  options: {
      scales: {
          y: {
              beginAtZero: true,
          },
      },
  },
});

// Expenses, Income, Budget Line Chart

const xValues = [100,200,300,400,500,600,700,800,900,1000];

new Chart(ctx3, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      data: [860,1140,1060,1060,1070,1110,1330,2210,7830,2478],
      borderColor: "red",
      fill: false
    },{
      data: [1600,1700,1700,1900,2000,2700,4000,5000,6000,7000],
      borderColor: "green",
      fill: false
    },{
      data: [300,700,2000,5000,6000,4000,2000,1000,200,100],
      borderColor: "blue",
      fill: false
    }]
  },
  options: {
    legend: {display: false}
  }
});

// doughnut chart Categories

var Values = ["Italy", "France", "Spain", "USA", "Argentina"];
var Values2 = [55, 49, 44, 24, 15];
var barColors = [
  "#b91d47",
  "#00aba9",
  "#2b5797",
  "#e8c3b9",
  "#1e7145"
];

new Chart(ctx4, {
  type: "doughnut",
  data: {
    labels: Values,
    datasets: [{
      backgroundColor: barColors,
      data: Values2
    }]
  },
  options: {
    title: {
      display: true,
      text: "World Wide Wine Production 2018"
    }
  }
});
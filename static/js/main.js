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
        labels: ["Food", "Decorations", "Guest Speakers", "Security", "Marketing", "Miscellaneous"],
        datasets: [
            {
                label: "Expenses in PHP",
                data: [5000, 2000, 3000, 1500, 2500, 1000].map(amount => amount * 50),
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
      labels: ["Ticket Sales", "Sponsorships", "Merchandise", "Food & Beverage Sales"],
      datasets: [
          {
              label: "Income in PHP",
              data: [6000, 4000, 2000, 3000].map(amount => amount * 50),
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
      labels: ["Initial Budget", "Final Expenditure", "Final Income"],
      datasets: [
          {
              label: "Budget in PHP",
              data: [15000, 13000, 15000].map(amount => amount * 50),
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

const xValues = ["Day 1","Day 2","Day 3","Day 4","Day 5","Day 6","Day 7"];

new Chart(ctx3, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      data: [2000, 2500, 3000, 3500, 4000, 4500, 5000].map(amount => amount * 50),
      borderColor: "red",
      fill: false,
      label: "Expenses"
    },{
      data: [1000, 2000, 3000, 4000, 5000, 6000, 7000].map(amount => amount * 50),
      borderColor: "green",
      fill: false,
      label: "Income"
    },{
      data: [15000, 13000, 11000, 9000, 7000, 5000, 3000].map(amount => amount * 50),
      borderColor: "blue",
      fill: false,
      label: "Budget"
    }]
  },
  options: {
    legend: {display: true}
  }
});

// Doughnut chart Categories

var Values = ["Engineering", "Arts", "Science", "Business", "Law"];
var Values2 = [200, 150, 180, 170, 100].map(amount => amount * 50);
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
      text: "Attendees by Faculty"
    }
  }
});
function showOffcanvas() {
    let offcanvasElement = document.getElementById("offcanvasExample");
    let offcanvas = new bootstrap.Offcanvas(offcanvasElement);
    offcanvas.show();
}

// Chart JS
const ctx = document.getElementById("myChart");
const ctx1 = document.getElementById("myChart1");
const ctx2 = document.getElementById("myChart2");
const ctx3 = document.getElementById("myChart3");
const ctx4 = document.getElementById("myChart4");

// Calculate total income and total expenses
let totalIncome = incomes.reduce((total, income) => total + income.amount, 0);
let totalExpenses = expenses.reduce((total, expense) => total + expense.amount, 0);

// Format as PHP currency
let formatter = new Intl.NumberFormat('en-PH', {
  style: 'currency',
  currency: 'PHP',
});

document.getElementById('totalIncome').textContent = formatter.format(totalIncome);
document.getElementById('totalExpenses').textContent = formatter.format(totalExpenses);

// Expenses Pie Chart
new Chart(ctx, {
  type: "pie",
  data: {
    labels: expenses.map(expense => expense.expense_name),
    datasets: [
      {
        label: "Expenses in PHP",
        data: expenses.map(expense => expense.amount),
        borderWidth: 1,
      },
    ],
  },
});

// Income Pie Chart
new Chart(ctx1, {
  type: "pie",
  data: {
    labels: incomes.map(income => income.income_name),
    datasets: [
      {
        label: "Income in PHP",
        data: incomes.map(income => income.amount * 50),
        borderWidth: 1,
      },
    ],
  },
});

// Budget Bar Chart
new Chart(ctx2, {
  type: "bar",
  data: {
    labels: ["Budget", "Total Income", "Total Expenses"],
    datasets: [
      {
        label: "Budget in PHP",
        data: [budget, totalIncome, totalExpenses],
        borderWidth: 1,
        backgroundColor: ['blue', 'green', 'red'],  // Add this line
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
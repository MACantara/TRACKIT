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
let totalIncome = incomes.reduce((total, income) => total + income.total_amount, 0);
let totalExpenses = expenses.reduce((total, expense) => total + expense.total_amount, 0);

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
        data: expenses.map(expense => expense.total_amount),
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
        data: incomes.map(income => income.total_amount),
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

let xValues = Array.from({length: 7}, (_, i) => {
  let d = new Date();
  d.setDate(d.getDate() + i);
  return `${d.getMonth()+1}/${d.getDate()}/${d.getFullYear()}`;
});

// Calculate daily totals for income and expenses
// Group incomes by date
let groupedIncomes = incomes.reduce((acc, income) => {
  let date = income.date;
  if (!acc[date]) {
    acc[date] = 0;
  }
  acc[date] += income.total_amount;
  return acc;
}, {});

// Convert grouped incomes to array
let dailyIncomes = Object.values(groupedIncomes);

// Group expenses by date
let groupedExpenses = expenses.reduce((acc, expense) => {
  let date = expense.date;
  if (!acc[date]) {
    acc[date] = 0;
  }
  acc[date] += expense.total_amount;
  return acc;
}, {});

// Convert grouped expenses to array
let dailyExpenses = Object.values(groupedExpenses);

// Calculate remaining budget for each day
let dailyBudget = Object.keys(groupedExpenses).map(date => {
  let expense = groupedExpenses[date] || 0;
  budget -= expense;
  return budget;
});

// Expenses, Income, Budget Line Chart
new Chart(ctx3, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      data: dailyExpenses,
      borderColor: "red",
      fill: false,
      label: "Expenses"
    },{
      data: dailyIncomes,
      borderColor: "green",
      fill: false,
      label: "Income"
    },{
      data: dailyBudget,
      borderColor: "blue",
      fill: false,
      label: "Remaining Budget"
    }]
  },
  options: {
    legend: {display: true},
    scales: {
      y: {
        ticks: {
          // Include a PHP sign in the ticks
          callback: function(value, index, values) {
            return 'PHP ' + value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
          }
        }
      }
    },
    responsive: true,
  }
});


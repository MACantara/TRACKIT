// Function to show offcanvas
function showOffcanvas() {
  let offcanvasElement = document.getElementById("offcanvasExample");
  let offcanvas = new bootstrap.Offcanvas(offcanvasElement);
  offcanvas.show();
}

// Chart JS
const chartElements = {
  expenses: document.getElementById("myChart"),
  incomes: document.getElementById("myChart1"),
  budget: document.getElementById("myChart2"),
  lineChart: document.getElementById("myChart3")
};

// Calculate total income and total expenses
let totalIncome = incomes.reduce((total, income) => total + income.amount, 0);
let totalExpenses = expenses.reduce((total, expense) => total + expense.amount, 0);

// Format as PHP currency
let formatter = new Intl.NumberFormat('en-PH', {
  style: 'currency',
  currency: 'PHP',
});

// Set total income and total expenses text
document.getElementById('totalIncome').textContent = formatter.format(totalIncome);
document.getElementById('totalExpenses').textContent = formatter.format(totalExpenses);

// Create pie chart for expenses
new Chart(chartElements.expenses, {
  type: "pie",
  data: {
    labels: expenses.map(expense => expense.expense_name),
    datasets: [{
      label: "Expenses in PHP",
      data: expenses.map(expense => expense.amount),
      borderWidth: 1,
    }],
  },
});

// Create pie chart for incomes
new Chart(chartElements.incomes, {
  type: "pie",
  data: {
    labels: incomes.map(income => income.income_name),
    datasets: [{
      label: "Income in PHP",
      data: incomes.map(income => income.amount),
      borderWidth: 1,
    }],
  },
});

// Create bar chart for budget
new Chart(chartElements.budget, {
  type: "bar",
  data: {
    labels: ["Budget", "Total Income", "Total Expenses"],
    datasets: [{
      label: "Budget in PHP",
      data: [budget, totalIncome, totalExpenses],
      borderWidth: 1,
      backgroundColor: ['blue', 'green', 'red'],
    }],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});

// Generate dates for the next 7 days
let xValues = Array.from({length: 7}, (_, i) => {
  let d = new Date();
  d.setDate(d.getDate() + i);
  return `${d.getMonth()+1}/${d.getDate()}/${d.getFullYear()}`;
});

// Group incomes and expenses by date
let groupedIncomes = groupByDate(incomes);
let groupedExpenses = groupByDate(expenses);

// Convert grouped incomes and expenses to arrays
let dailyIncomes = Object.values(groupedIncomes);
let dailyExpenses = Object.values(groupedExpenses);

// Calculate remaining budget for each day
let dailyBudget = calculateDailyBudget(groupedExpenses);

// Create line chart for expenses, income, and remaining budget
new Chart(chartElements.lineChart, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [
      createDataset(dailyExpenses, "red", "Expenses"),
      createDataset(dailyIncomes, "green", "Income"),
      createDataset(dailyBudget, "blue", "Remaining Budget")
    ]
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

// Helper function to group amounts by date
function groupByDate(items) {
  return items.reduce((acc, item) => {
    let date = item.date;
    if (!acc[date]) {
      acc[date] = 0;
    }
    acc[date] += item.amount;
    return acc;
  }, {});
}

// Helper function to calculate daily budget
function calculateDailyBudget(groupedExpenses) {
  return Object.keys(groupedExpenses).map(date => {
    let expense = groupedExpenses[date] || 0;
    budget -= expense;
    return budget;
  });
}

// Helper function to create dataset for line chart
function createDataset(data, color, label) {
  return {
    data: data,
    borderColor: color,
    fill: false,
    label: label
  };
}
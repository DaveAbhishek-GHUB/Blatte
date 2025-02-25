// Add at the beginning of the file
async function fetchDashboardData() {
    try {
        const response = await fetch('/admin/dashboard-data');
        const data = await response.json();
        
        // Initialize charts with the fetched data
        initializeUserGrowthChart(data.userGrowth);
        initializeOrderGrowthChart(data.orderGrowth);
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
    }
}

// Update the DOMContentLoaded event
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather icons
    feather.replace();
    
    // Fetch and initialize charts
    fetchDashboardData();
});

// Update the chart initialization functions to accept data
function initializeUserGrowthChart(data) {
    const ctx = document.getElementById('userGrowthChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    type: 'bar',
                    label: 'User Growth',
                    data: data.data,
                    backgroundColor: 'rgba(0, 0, 255, 0.6)',
                    order: 1
                },
                {
                    type: 'line',
                    label: 'Growth Rate',
                    data: data.data,
                    borderColor: 'rgb(0, 200, 0)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    order: 0
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
}

function initializeOrderGrowthChart(data) {
    const ctx = document.getElementById('orderGrowthChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    type: 'bar',
                    label: 'Order Growth',
                    data: data.data,
                    backgroundColor: 'rgba(255, 165, 0, 0.6)',
                    order: 1
                },
                {
                    type: 'line',
                    label: 'Growth Rate',
                    data: data.data,
                    borderColor: 'rgb(255, 255, 0)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    order: 0
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
}

// Sales Overview Chart
function initializeSalesChart() {
    const ctx = document.getElementById('salesChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Sales',
                data: salesData, // This will come from your Flask route
                borderColor: '#6c5ce7',
                tension: 0.4,
                fill: true,
                backgroundColor: 'rgba(108, 92, 231, 0.1)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Product Categories Chart
function initializeCategoryChart() {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: categoryLabels, // This will come from your Flask route
            datasets: [{
                data: categoryData, // This will come from your Flask route
                backgroundColor: [
                    '#6c5ce7',
                    '#00cec9',
                    '#fd79a8',
                    '#fdcb6e',
                    '#55efc4'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

// Revenue Trends Chart
function initializeRevenueChart() {
    const ctx = document.getElementById('revenueChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: revenueLabels, // This will come from your Flask route
            datasets: [{
                label: 'Revenue',
                data: revenueData, // This will come from your Flask route
                backgroundColor: '#6c5ce7',
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
} 
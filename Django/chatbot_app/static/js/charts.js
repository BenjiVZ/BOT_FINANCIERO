// This file should be placed in your Django project's static files directory
// Typically: yourapp/static/js/charts.js

document.addEventListener('DOMContentLoaded', function() {
    // Gráfico de Gastos por Categoría
    const ctxCategorias = document.getElementById('chartCategorias').getContext('2d');
    const dataCategorias = {
        labels: JSON.parse(document.getElementById('datos_categorias').textContent),
        datasets: [{
            label: 'Gastos por Categoría',
            data: JSON.parse(document.getElementById('totales_categorias').textContent),
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    };
    new Chart(ctxCategorias, {
        type: 'bar',
        data: dataCategorias,
        options: { scales: { y: { beginAtZero: true } } }
    });

    // Gráfico de Ingresos y Gastos Mensuales
    const ctxIngresosGastos = document.getElementById('chartIngresosGastos').getContext('2d');
    const dataIngresosGastos = {
        labels: JSON.parse(document.getElementById('meses').textContent),
        datasets: [
            {
                label: 'Ingresos',
                data: JSON.parse(document.getElementById('ingresos_mensuales').textContent),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            },
            {
                label: 'Gastos',
                data: JSON.parse(document.getElementById('gastos_mensuales').textContent),
                backgroundColor: 'rgba(255, 99, 132, 0.6)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }
        ]
    };
    new Chart(ctxIngresosGastos, {
        type: 'line',
        data: dataIngresosGastos,
        options: { scales: { y: { beginAtZero: true } } }
    });

    // Gráfico de Balance Mensual
    const ctxBalanceMensual = document.getElementById('chartBalanceMensual').getContext('2d');
    const dataBalanceMensual = {
        labels: JSON.parse(document.getElementById('meses_balance').textContent),
        datasets: [{
            label: 'Balance Mensual',
            data: JSON.parse(document.getElementById('balances_mensuales').textContent),
            backgroundColor: 'rgba(153, 102, 255, 0.6)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
        }]
    };
    new Chart(ctxBalanceMensual, {
        type: 'bar',
        data: dataBalanceMensual,
        options: { scales: { y: { beginAtZero: true } } }
    });
});

        // Gráfico de Gastos por Categoría
        const ctxCategorias = document.getElementById('chartCategorias').getContext('2d');
        const dataCategorias = {
            labels: [{% for item in datos_categorias %}"{{ item.categoria__nombre }}"{% if not forloop.last %}, {% endif %} {% endfor %}],
        datasets: [{
            label: 'Gastos por Categoría',
            data: [{% for item in datos_categorias %}{{ item.total }}{% if not forloop.last %}, {% endif %} {% endfor %}],
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
            labels: [{% for ingreso in ingresos_mensuales %}{{ ingreso.fecha__month }}{% if not forloop.last %}, {% endif %} {% endfor %}],
        datasets: [
            {
                label: 'Ingresos',
                data: [{% for ingreso in ingresos_mensuales %}{{ ingreso.total }}{% if not forloop.last %}, {% endif %} {% endfor %}],
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
                },
        {
            label: 'Gastos',
                data: [{% for gasto in gastos_mensuales %} { { gasto.total } } {% if not forloop.last %}, {% endif %} {% endfor %}],
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
            labels: [{% for balance in balances_mensuales %}"{{ balance.mes }}"{% if not forloop.last %}, {% endif %} {% endfor %}],
        datasets: [{
            label: 'Balance Mensual',
            data: [{% for balance in balances_mensuales %}{{ balance.balance }}{% if not forloop.last %}, {% endif %} {% endfor %}],
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
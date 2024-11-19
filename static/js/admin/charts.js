// External JavaScript for rendering the chart
document.addEventListener('DOMContentLoaded', function () {
    // Ensure the chartData is available globally
    if (window.chartData) {
        const bespoke_order_options = {
            series: window.chartData.series,
            colors: ['#3C21F7', '#FFCA1F', '#00E396'],  // Customize the colors if needed
            chart: {
                height: 300,
                type: 'line',
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            xaxis: {
                categories: window.chartData.categories,
            },
        };

        // Initialize the chart
        let bespoke_order_chart = new ApexCharts(document.querySelector("#bespoke_order-chart"), bespoke_order_options);
        bespoke_order_chart.render();
    }
});


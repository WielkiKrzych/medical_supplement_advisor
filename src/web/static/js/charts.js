function renderTestCharts(analysisData) {
    if (!analysisData) return;

    const categories = [
        { key: "inflammatory_markers", title: "Markery zapalne" },
        { key: "minerals_vitamins", title: "Składniki mineralne i witaminy" },
        { key: "electrolytes", title: "Elektrolity" }
    ];

    categories.forEach(function(category) {
        var tests = analysisData[category.key];
        if (!tests || tests.length === 0) return;

        var canvas = document.getElementById("chart-" + category.key);
        if (!canvas) return;

        var labels = tests.map(function(t) { return t.name; });
        var values = tests.map(function(t) { return t.value; });
        var barColors = tests.map(function(t) {
            if (t.status === "high") return "rgba(239, 68, 68, 0.8)";
            if (t.status === "low") return "rgba(59, 130, 246, 0.8)";
            return "rgba(34, 197, 94, 0.8)";
        });

        var annotations = {};
        tests.forEach(function(t, i) {
            if (t.lab_reference && (t.lab_reference.min !== null || t.lab_reference.max !== null)) {
                annotations["ref_" + i] = {
                    type: "box",
                    yScaleID: "y",
                    yMin: i - 0.35,
                    yMax: i + 0.35,
                    xMin: t.lab_reference.min || 0,
                    xMax: t.lab_reference.max || t.value * 2,
                    backgroundColor: "rgba(34, 197, 94, 0.1)",
                    borderColor: "rgba(34, 197, 94, 0.3)",
                    borderWidth: 1
                };
            }
            if (t.optimal_range && (t.optimal_range.min !== null || t.optimal_range.max !== null)) {
                annotations["opt_" + i] = {
                    type: "box",
                    yScaleID: "y",
                    yMin: i - 0.2,
                    yMax: i + 0.2,
                    xMin: t.optimal_range.min || 0,
                    xMax: t.optimal_range.max || t.value * 2,
                    backgroundColor: "rgba(34, 197, 94, 0.2)",
                    borderColor: "rgba(34, 197, 94, 0.5)",
                    borderWidth: 1
                };
            }
        });

        new Chart(canvas, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: category.title,
                    data: values,
                    backgroundColor: barColors,
                    borderColor: barColors.map(function(c) { return c.replace("0.8", "1"); }),
                    borderWidth: 1,
                    barPercentage: 0.6
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    annotation: {
                        annotations: annotations
                    }
                },
                scales: {
                    x: {
                        beginAtZero: false,
                        grid: { color: "rgba(0,0,0,0.05)" }
                    },
                    y: {
                        grid: { display: false }
                    }
                }
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", function() {
    renderTestCharts(window.analysisData);
});

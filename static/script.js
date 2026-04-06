/**
 * Intern Performance System - v1.0.1
 */
document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const resultsCard = document.getElementById('results-card');
    const loader = document.getElementById('loader');
    const resultsTableBody = document.querySelector('#results-table tbody');
    const chartPlaceholder = document.getElementById('chart-placeholder');
    const downloadBtn = document.getElementById('download-btn');
    
    let performanceChart = null;
    let lastResults = null;

    // Handle Drag & Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    async function handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);

        showLoader(true);

        try {
            const response = await fetch('/predict_batch', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            const results = await response.json();
            lastResults = results;
            renderResults(results);
        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        } finally {
            showLoader(false);
        }
    }

    function renderResults(results) {
        // Show results sections
        resultsCard.classList.remove('hidden');
        chartPlaceholder.classList.add('hidden');

        // Clear existing table data
        resultsTableBody.innerHTML = '';

        // Prepare chart data
        const labels = results.map(r => r.intern_id);
        const scores = results.map(r => r.predicted_performance);
        
        // Update Table
        results.forEach(result => {
            const row = document.createElement('tr');
            const level = getPerformanceLevel(result.predicted_performance);
            row.innerHTML = `
                <td><strong>${result.intern_id}</strong></td>
                <td>${result.predicted_performance.toFixed(2)}%</td>
                <td><span class="badge badge-${level.toLowerCase()}">${level}</span></td>
            `;
            resultsTableBody.appendChild(row);
        });

        // Update Chart
        updateChart(labels, scores);
        
        // Scroll to results
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function getPerformanceLevel(score) {
        if (score >= 90) return 'Exceptional';
        if (score >= 75) return 'High';
        if (score >= 50) return 'Moderate';
        return 'Needs Improvement';
    }

    function updateChart(labels, data) {
        const ctx = document.getElementById('performanceChart').getContext('2d');
        
        if (performanceChart) {
            performanceChart.destroy();
        }

        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, '#6366f1');
        gradient.addColorStop(1, '#a855f7');

        performanceChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Predicted Performance (%)',
                    data: data,
                    backgroundColor: gradient,
                    borderRadius: 8,
                    borderWidth: 0,
                    barThickness: 30
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    }
                }
            }
        });
    }

    function showLoader(show) {
        if (show) {
            loader.classList.remove('hidden');
        } else {
            loader.classList.add('hidden');
        }
    }

    // Basic CSV Download logic
    downloadBtn.addEventListener('click', () => {
        if (!lastResults) return;
        
        let csvContent = "data:text/csv;charset=utf-8,Intern ID,Predicted Score\n";
        lastResults.forEach(r => {
            csvContent += `${r.intern_id},${r.predicted_performance}\n`;
        });

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "performance_predictions.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
});

(function () {
    document.addEventListener('DOMContentLoaded', () => {
        let graficoGlobal = null;

    // ===== CALCULAR TENDENCIA =====
    async function calcularTendencia(scoreActual) {
        const res = await fetch('/api/historico?limit=2');
        const data = await res.json();
        const valores = data.historico.reverse();

        if (valores.length < 2) return { texto: '→ Estable', color: '#555' };

        const anterior = valores[valores.length - 2].ecoscore;
        const diferencia = scoreActual - anterior;

        if (diferencia > 5) return { texto: '↗ Mejora', color: '#2e7d32' };
        if (diferencia < -5) return { texto: '↘ Empeora', color: '#c62828' };
        return { texto: '→ Estable', color: '#555' };
    }

    // ===== ÚLTIMO ECOSCORE =====
    async function cargarUltimo() {
        try {
            const res = await fetch('/api/ultimo');
            const data = await res.json();

            if (data.status === 'sin_datos') {
                document.getElementById('ultimo').innerText = 'No hay datos aún';
                return;
            }

            const score = data.ecoscore;
            document.getElementById('ultimo').innerText = `${score.toFixed(2)} (${data.timestamp})`;

            // Clasificación
            let estado = '', clase = '';
            if (score < 200) { estado = 'Crítico'; clase = 'critical'; }
            else if (score < 350) { estado = 'Moderado'; clase = 'moderate'; }
            else if (score < 450) { estado = 'Bueno'; clase = 'good'; }
            else { estado = 'Excelente'; clase = 'excellent'; }

            const estadoElem = document.getElementById('estado');
            if (estadoElem) {
                estadoElem.innerText = estado;
                estadoElem.className = 'eco-state ' + clase;
            }

            // Tendencia
            const tendenciaElem = document.getElementById('tendencia');
            const tendencia = await calcularTendencia(score);
            if (tendenciaElem) {
                tendenciaElem.innerText = tendencia.texto;
                tendenciaElem.style.color = tendencia.color;
            }

            // Alerta
            const alerta = document.getElementById('alerta');
            const card = document.getElementById('card-principal');
            const sonido = document.getElementById('alerta-sound');

            try { if (sonido) { sonido.currentTime = 0; sonido.play(); } } catch(e){}

            if(score < 200) {
                if(alerta) alerta.style.display = 'block';
                if(card) card.style.border = '3px solid #e53935';
            } else {
                if(alerta) alerta.style.display = 'none';
                if(card) card.style.border = 'none';
            }

        } catch(err) {
            console.error('Error cargando último ecoscore:', err);
        }
    }

    // ===== HISTORIAL =====
    async function cargarHistorial() {
        const res = await fetch('/api/historico?limit=30');
        const data = await res.json();
        return data.historico.reverse();
    }

    // ===== GRAFICO =====
    async function dibujarGrafico() {
        try {
            const historial = await cargarHistorial();
            const labels = historial.map(x => x.timestamp);
            const valores = historial.map(x => Number(x.ecoscore));

            const canvas = document.getElementById('grafico');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');

            if (graficoGlobal !== null) graficoGlobal.destroy();

            graficoGlobal = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'EcoScore',
                        data: valores,
                        borderWidth: 3,
                        tension: 0.3,
                        borderColor: '#666',
                        pointBackgroundColor: '#444',
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    animation: false,
                    scales: { y: { beginAtZero: true, max: 500 } }
                }
            });
        } catch(err) {
            console.error('Error dibujando gráfico:', err);
        }
    }

    // ===== AUTO-REFRESCO =====
    setInterval(() => { cargarUltimo(); dibujarGrafico(); }, 60000);

    // ===== MODAL DE TABLA =====
    const btnAbrirTabla = document.querySelector("#btn-tabla");
    const btnCerrarTabla = document.querySelector("#cerrar-tabla");
    const modalTabla = document.querySelector("#modal-tabla");

    if (btnAbrirTabla && modalTabla) btnAbrirTabla.addEventListener("click", () => modalTabla.showModal());
    if (btnCerrarTabla && modalTabla) btnCerrarTabla.addEventListener("click", () => modalTabla.close());

    // ===== TABS CON ANIMACIÓN =====
    const tabs = document.querySelectorAll(".tab-buttons button");
    const loader = document.querySelector("#loader");

    tabs.forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.dataset.tab;
            const current = document.querySelector(".tab-content.active");
            if(current && current.id === target) return;

            if (loader) loader.classList.add("show");
            if (current) current.style.opacity = 0;

            setTimeout(() => {
                if (current) {
                    current.classList.remove("active");
                    current.style.display = "none";
                }

                const newTab = document.getElementById(target);
                if (newTab) newTab.style.display = "block";

                setTimeout(() => {
                    if (newTab) newTab.classList.add("active");
                    if (loader) loader.classList.remove("show");
                }, 50);
            }, 1000);
        });
    });

        // ===== LLAMADAS INICIALES =====
        cargarUltimo();
        dibujarGrafico();

        // exportar funciones globalmente
        window._eco = { cargarUltimo, dibujarGrafico };
    });
})();

// API Base URL
const API_URL = "http://localhost:8000/api";
const BACKEND_URL = "http://localhost:8000";

// Estado global
let allConcursantes = [];
let allLevantamientos = [];
let currentRankingFilter = 'all';
let currentCompetitionFilter = 'all';
let currentSort = 'ipf';

// ==================== FUNCIONES DE INICIALIZACIÓN ====================

document.addEventListener('DOMContentLoaded', () => {
    loadAllData();
    setInterval(loadAllData, 30000); // Actualizar cada 30 segundos
});

async function loadAllData() {
    await loadConcursantes();
    await loadLevantamientos();
    await loadStats();
    await loadTopPerformers();
    await loadCompetitions();
    await loadResults();
    await loadRecords();
}

// ==================== CARGA DE DATOS ====================

async function loadConcursantes() {
    try {
        const response = await fetch(`${API_URL}/concursantes`);
        if (!response.ok) throw new Error('Error al cargar concursantes');
        allConcursantes = await response.json();
        displayConcursantes();
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar concursantes', 'error');
    }
}

async function loadLevantamientos() {
    try {
        const response = await fetch(`${API_URL}/levantamientos`);
        if (!response.ok) throw new Error('Error al cargar levantamientos');
        allLevantamientos = await response.json();
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/estadisticas`);
        if (!response.ok) throw new Error('Error al cargar estadísticas');
        const stats = await response.json();
        
        document.getElementById('stat-concursantes').textContent = stats.total_concursantes;
        document.getElementById('stat-competiciones').textContent = stats.total_competiciones;
        document.getElementById('stat-levantamientos').textContent = stats.total_levantamientos;
        document.getElementById('stat-mejor-ipf').textContent = stats.mejor_ipf.toFixed(2);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadTopPerformers() {
    try {
        const response = await fetch(`${API_URL}/ranking`);
        if (!response.ok) throw new Error('Error al cargar ranking');
        const ranking = await response.json();
        
        const top5 = ranking.slice(0, 5);
        const tbody = document.querySelector('#top-performers-table tbody');
        tbody.innerHTML = '';
        
        top5.forEach((performer, index) => {
            const row = `
                <tr>
                    <td><strong>${index + 1}</strong></td>
                    <td>${performer.nombre}</td>
                    <td>${performer.categoria_peso} kg (${performer.sexo})</td>
                    <td>${performer.total}</td>
                    <td><span style="color: #e74c3c; font-weight: bold;">${performer.ipf_score.toFixed(2)}</span></td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadResults() {
    try {
        const response = await fetch(`${API_URL}/ranking`);
        if (!response.ok) throw new Error('Error al cargar resultados');
        const results = await response.json();
        const tbody = document.querySelector('#results-table tbody');
        if (!tbody) return;
        tbody.innerHTML = '';
        results.slice(0, 10).forEach((item, index) => {
            const row = `
                <tr>
                    <td>${index + 1}</td>
                    <td>${item.nombre}</td>
                    <td>${item.categoria_peso} kg</td>
                    <td>${item.sentadilla}</td>
                    <td>${item.press_banca}</td>
                    <td>${item.peso_muerto}</td>
                    <td><strong>${item.total}</strong></td>
                    <td>${item.ipf_score.toFixed(2)}</td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// ==================== DISPLAY FUNCTIONS ====================

function displayConcursantes() {
    const grid = document.getElementById('concursantes-grid');
    grid.innerHTML = '';
    
    allConcursantes.forEach(concursante => {
        const levantamientos = allLevantamientos.filter(l => l.concursante_id === concursante.id);
        const mejorIPF = levantamientos.length > 0 
            ? Math.max(...levantamientos.map(l => l.ipf_score))
            : 0;
        const photoSrc = concursante.photo_url ? (BACKEND_URL + concursante.photo_url) : '';
        
        const card = `
            <div class="concursante-card">
                <h3>${concursante.nombre}</h3>
                ${photoSrc ? `<img src="${photoSrc}" alt="foto" style="width:80px;height:100px;object-fit:cover;border-radius:6px;margin-bottom:10px;">` : ''}
                <div class="concursante-info">
                    <p><strong>Edad:</strong> ${concursante.edad} años</p>
                    <p><strong>Peso:</strong> ${concursante.peso_corporal} kg</p>
                    <p><strong>Sexo:</strong> ${concursante.sexo === 'M' ? 'Masculino' : 'Femenino'}</p>
                    <p><strong>Categoría:</strong> ${concursante.categoria_peso} kg</p>
                    <p><strong>Club:</strong> ${concursante.club || 'N/A'}</p>
                    <p><strong>Ciudad:</strong> ${concursante.ciudad || 'N/A'}</p>
                    <p><strong>Desde:</strong> ${concursante.ano_inicio || 'N/A'}</p>
                    <p><strong>Levantamientos:</strong> ${levantamientos.length}</p>
                    ${mejorIPF > 0 ? `<span class="concursante-badge">Mejor IPF: ${mejorIPF.toFixed(2)}</span>` : ''}
                </div>
            </div>
        `;
        grid.innerHTML += card;
    });
}

// ==================== NAVEGACIÓN ====================

function switchTab(tabName) {
    // Ocultar todos los tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remover active de botones
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Mostrar tab activo
    document.getElementById(tabName).classList.add('active');
    
    // Marcar botón como activo
    event.target.classList.add('active');
    
    // Cargar datos específicos según el tab
    if (tabName === 'ranking') {
        loadRanking('all');
    } else if (tabName === 'records') {
        loadRecords();
    } else if (tabName === 'resultados') {
        loadResults();
    } else if (tabName === 'competencias') {
        loadCompetitions();
    }
}

// ==================== RANKING ====================

function filterRanking(category) {
    currentRankingFilter = category;
    
    // Actualizar botones activos
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    loadRanking(category);
}

async function loadRanking(category) {
    try {
        let url = `${API_URL}/ranking`;
        if (category !== 'all') {
            url += `/${category}`;
        }
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('Error al cargar ranking');
        const ranking = await response.json();
        
        const tbody = document.querySelector('#ranking-table tbody');
        tbody.innerHTML = '';
        
        ranking.forEach((item, index) => {
            const row = `
                <tr>
                    <td>${index + 1}</td>
                    <td>${item.nombre}</td>
                    <td>${item.sexo === 'M' ? 'Masculino' : 'Femenino'}</td>
                    <td>${item.categoria_peso} kg</td>
                    <td>${item.sentadilla}</td>
                    <td>${item.press_banca}</td>
                    <td>${item.peso_muerto}</td>
                    <td><strong>${item.total}</strong></td>
                    <td><span style="color: #e74c3c; font-weight: bold;">${item.ipf_score.toFixed(2)}</span></td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar ranking', 'error');
    }
}

// ==================== AGREGAR CONCURSANTE ====================

async function addConcursante(event) {
    event.preventDefault();
    
    const concursante = {
        nombre: document.getElementById('nombre').value,
        edad: parseInt(document.getElementById('edad').value),
        peso_corporal: parseFloat(document.getElementById('peso_corporal').value),
        sexo: document.getElementById('sexo').value,
        categoria_peso: document.getElementById('categoria_peso').value,
        club: document.getElementById('club').value || '',
        ciudad: document.getElementById('ciudad').value || '',
        ano_inicio: parseInt(document.getElementById('ano_inicio').value) || new Date().getFullYear()
    };
    
    try {
        const response = await fetch(`${API_URL}/concursantes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(concursante)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al agregar concursante');
        }
        
        showToast('¡Concursante registrado exitosamente!', 'success');
        document.getElementById('form-concursante').reset();
        const created = await response.json();
        // Si se subió foto, enviarla
        const photoInput = document.getElementById('photo');
        if (photoInput && photoInput.files && photoInput.files.length > 0) {
            const form = new FormData();
            form.append('file', photoInput.files[0]);
            try {
                await fetch(`${API_URL.replace('/api','')}/api/concursantes/${created.id}/photo`, {
                    method: 'POST',
                    body: form
                });
            } catch (err) { console.error('Error subiendo foto', err); }
        }
        await loadAllData();
    } catch (error) {
        console.error('Error:', error);
        showToast(error.message || 'Error al registrar concursante', 'error');
    }
}

async function loadCompetitions() {
    try {
        const response = await fetch(`${API_URL}/competiciones`);
        if (!response.ok) return;
        const comps = await response.json();
        const sel = document.getElementById('competition-filter');
        const list = document.getElementById('competitions-list');
        if (sel) sel.innerHTML = '<option value="all">Todas</option>';
        if (list) list.innerHTML = '';
        comps.forEach(c => {
            if (sel) {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = `${c.nombre} (${new Date(c.fecha).toLocaleDateString()})`;
                sel.appendChild(opt);
            }
            if (list) {
                const card = document.createElement('article');
                card.className = 'info-card';
                card.innerHTML = `
                    <h3>${c.nombre}</h3>
                    <p><strong>Fecha:</strong> ${new Date(c.fecha).toLocaleDateString()}</p>
                    <p><strong>Ubicación:</strong> ${c.ubicacion}</p>
                    <p>${c.descripcion || 'Competencia oficial registrada en la plataforma.'}</p>
                `;
                list.appendChild(card);
            }
        });
    } catch (err) {
        console.error(err);
    }
}

function filterByCompetition() {
    const val = document.getElementById('competition-filter').value;
    currentCompetitionFilter = val;
    if (val === 'all') {
        loadRanking(currentRankingFilter);
        return;
    }
    loadRankingByCompetition(val);
}

async function loadRankingByCompetition(compId) {
    try {
        const response = await fetch(`${API_URL}/competiciones/${compId}`);
        if (!response.ok) throw new Error('Error al cargar competición');
        const comp = await response.json();
        const levs = comp.levantamientos || [];
        renderRankingTable(levs.map(l => ({
            nombre: l.concursante.nombre,
            sexo: l.concursante.sexo,
            categoria_peso: l.concursante.categoria_peso,
            sentadilla: l.sentadilla,
            press_banca: l.press_banca,
            peso_muerto: l.peso_muerto,
            total: l.sentadilla + l.press_banca + l.peso_muerto,
            ipf_score: l.ipf_score
        })));
    } catch (err) { console.error(err); showToast('Error al cargar competición', 'error'); }
}

function applySort() {
    currentSort = document.getElementById('sort-filter').value;
    if (currentCompetitionFilter === 'all') {
        loadRanking(currentRankingFilter);
    } else {
        loadRankingByCompetition(currentCompetitionFilter);
    }
}

function renderRankingTable(items) {
    const tbody = document.querySelector('#ranking-table tbody');
    tbody.innerHTML = '';
    // ordenar
    items.sort((a,b) => (currentSort === 'ipf' ? b.ipf_score - a.ipf_score : (b.total || 0) - (a.total || 0)));
    items.forEach((item, index) => {
        const row = `
            <tr>
                <td>${index + 1}</td>
                <td>${item.nombre}</td>
                <td>${item.sexo === 'M' ? 'Masculino' : 'Femenino'}</td>
                <td>${item.categoria_peso} kg</td>
                <td>${item.sentadilla}</td>
                <td>${item.press_banca}</td>
                <td>${item.peso_muerto}</td>
                <td><strong>${item.total}</strong></td>
                <td><span style="color: #e74c3c; font-weight: bold;">${item.ipf_score.toFixed(2)}</span></td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

async function loadRecords() {
    try {
        const response = await fetch(`${API_URL}/records`);
        if (!response.ok) throw new Error('Error al cargar records');
        const records = await response.json();
        const tbody = document.querySelector('#records-table tbody');
        if (!tbody) return;
        tbody.innerHTML = '';
        records.forEach(record => {
            const row = `
                <tr>
                    <td>${record.categoria} kg</td>
                    <td>${record.concursante}</td>
                    <td>${record.sentadilla}</td>
                    <td>${record.press_banca}</td>
                    <td>${record.peso_muerto}</td>
                    <td><strong>${record.total}</strong></td>
                    <td>${record.ipf_score.toFixed(2)}</td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (err) { console.error(err); showToast('Error al cargar records', 'error'); }
}

// ==================== FILTRO DE BÚSQUEDA ====================

function filterConcursantes() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const cards = document.querySelectorAll('.concursante-card');
    
    cards.forEach(card => {
        const nombre = card.querySelector('h3').textContent.toLowerCase();
        if (nombre.includes(searchTerm)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

// ==================== NOTIFICACIONES ====================

function showToast(message, type = 'success') {
    // Crear elemento toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: ${type === 'success' ? '#cfe7d9' : '#f7d6d6'};
        color: #4a5a66;
        padding: 15px 20px;
        border-radius: 5px;
        font-weight: bold;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Agregar estilos de animación
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(24px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(24px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

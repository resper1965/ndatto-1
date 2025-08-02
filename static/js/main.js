// Função para atualizar a data/hora da última atualização
function updateLastUpdate() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('pt-BR');
    const lastUpdateElement = document.getElementById('last-update');
    if (lastUpdateElement) {
        lastUpdateElement.textContent = timeString;
    }
}

// Função para confirmar ações
function confirmAction(message) {
    return confirm(message || 'Tem certeza que deseja continuar?');
}

// Função para mostrar notificações
function showNotification(message, type = 'info') {
    const alertClass = type === 'error' ? 'alert-danger' : 
                      type === 'success' ? 'alert-success' : 
                      type === 'warning' ? 'alert-warning' : 'alert-info';
    
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Insere no topo da página
    const container = document.querySelector('main');
    if (container) {
        container.insertAdjacentHTML('afterbegin', alertHtml);
    }
}

// Função para atualizar dados em tempo real (placeholder)
function startRealTimeUpdates() {
    // TODO: Implementar atualizações em tempo real via WebSocket ou polling
    setInterval(updateLastUpdate, 60000); // Atualiza a cada minuto
}

// Função para formatar datas
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR');
}

// Função para formatar status
function formatStatus(status) {
    const statusMap = {
        'online': 'Online',
        'offline': 'Offline',
        'new': 'Novo',
        'resolved': 'Resolvido',
        'active': 'Ativo',
        'inactive': 'Inativo'
    };
    
    return statusMap[status] || status;
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Atualiza a última atualização
    updateLastUpdate();
    
    // Inicia atualizações em tempo real
    startRealTimeUpdates();
    
    // Adiciona listeners para confirmações
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirmAction(message)) {
                e.preventDefault();
            }
        });
    });
    
    // Adiciona listeners para formulários de filtro
    const filterForms = document.querySelectorAll('form[method="GET"]');
    filterForms.forEach(form => {
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                form.submit();
            });
        });
    });
});

// Função para fazer logout
function logout() {
    if (confirmAction('Tem certeza que deseja sair?')) {
        window.location.href = '/logout';
    }
}

// Função para atualizar dashboard
function refreshDashboard() {
    window.location.reload();
}

// Exporta funções para uso global
window.showNotification = showNotification;
window.formatDate = formatDate;
window.formatStatus = formatStatus;
window.logout = logout;
window.refreshDashboard = refreshDashboard; 
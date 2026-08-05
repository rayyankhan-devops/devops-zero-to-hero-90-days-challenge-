document.addEventListener('DOMContentLoaded', () => {
  const dbStatusBadge = document.getElementById('db-status-badge');
  const dbStatusText = document.getElementById('db-status-text');
  const infoDbHost = document.getElementById('info-db-host');

  const itemForm = document.getElementById('item-form');
  const itemTitle = document.getElementById('item-title');
  const itemDesc = document.getElementById('item-desc');
  const submitBtn = document.getElementById('submit-btn');

  const seedBtn = document.getElementById('seed-btn');
  const refreshBtn = document.getElementById('refresh-btn');
  const itemsContainer = document.getElementById('items-container');
  const toast = document.getElementById('toast');

  let isConnected = false;

  // Show Toast Notification
  function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast toast-${type}`;
    toast.classList.remove('hidden');

    setTimeout(() => {
      toast.classList.add('hidden');
    }, 4000);
  }

  // Check Database & Backend Health
  async function checkHealth() {
    try {
      const res = await fetch('/api/health');
      const data = await res.json();

      if (data.db_connected) {
        isConnected = true;
        dbStatusBadge.className = 'badge badge-connected';
        dbStatusText.textContent = 'MariaDB Connected';
        infoDbHost.textContent = `${data.db_host} (${data.db_name})`;
      } else {
        isConnected = false;
        dbStatusBadge.className = 'badge badge-disconnected';
        dbStatusText.textContent = 'MariaDB Disconnected';
        infoDbHost.textContent = `${data.db_host} (Unavailable)`;
      }
    } catch (err) {
      isConnected = false;
      dbStatusBadge.className = 'badge badge-disconnected';
      dbStatusText.textContent = 'Backend Offline';
      infoDbHost.textContent = 'Server Offline';
    }
  }

  // Fetch Items from MariaDB
  async function fetchItems() {
    itemsContainer.innerHTML = `
      <div class="loading-state">
        <div class="spinner"></div>
        <p>Fetching records from MariaDB...</p>
      </div>
    `;

    try {
      const res = await fetch('/api/items');
      const result = await res.json();

      if (!res.ok || !result.success) {
        renderErrorState(result.message || 'Failed to connect to database server.');
        return;
      }

      const items = result.data || [];
      renderItems(items);
    } catch (err) {
      renderErrorState('Network error connecting to backend API.');
    }
  }

  // Render items grid
  function renderItems(items) {
    if (items.length === 0) {
      itemsContainer.innerHTML = `
        <div class="empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          <p>No records found in MariaDB yet.<br>Create a new entry above or click "Add Sample Entry".</p>
        </div>
      `;
      return;
    }

    itemsContainer.innerHTML = items.map(item => {
      const date = item.created_at ? new Date(item.created_at).toLocaleString() : 'Just now';
      return `
        <div class="item-card" data-id="${item.id}">
          <div class="item-content">
            <h3>${escapeHtml(item.title)}</h3>
            ${item.description ? `<p>${escapeHtml(item.description)}</p>` : ''}
            <div class="item-meta">
              <span>ID: #${item.id}</span>
              <span>&bull;</span>
              <span>${date}</span>
            </div>
          </div>
          <button class="btn-delete" onclick="deleteItem(${item.id})" title="Delete Record">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"></path>
            </svg>
          </button>
        </div>
      `;
    }).join('');
  }

  function renderErrorState(message) {
    itemsContainer.innerHTML = `
      <div class="empty-state">
        <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <p style="color: var(--danger); font-weight: 500;">${escapeHtml(message)}</p>
      </div>
    `;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, function(m) {
      return {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
      }[m];
    });
  }

  // Create Item Form Handler
  itemForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = itemTitle.value.trim();
    const description = itemDesc.value.trim();

    if (!title) return;

    submitBtn.disabled = true;
    submitBtn.innerText = 'Saving...';

    try {
      const res = await fetch('/api/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description })
      });

      const result = await res.json();

      if (res.ok && result.success) {
        showToast('Record saved to MariaDB!', 'success');
        itemTitle.value = '';
        itemDesc.value = '';
        fetchItems();
      } else {
        showToast(result.message || 'Failed to save record.', 'error');
      }
    } catch (err) {
      showToast('Network error while saving item.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Save to MariaDB
      `;
    }
  });

  // Delete Item Handler (Global window function)
  window.deleteItem = async function(id) {
    if (!confirm(`Are you sure you want to delete record #${id}?`)) return;

    try {
      const res = await fetch(`/api/items?id=${id}`, {
        method: 'DELETE'
      });

      const result = await res.json();

      if (res.ok && result.success) {
        showToast(`Record #${id} deleted`, 'success');
        fetchItems();
      } else {
        showToast(result.message || 'Failed to delete record.', 'error');
      }
    } catch (err) {
      showToast('Network error deleting record.', 'error');
    }
  };

  // Seed Sample Entry
  const samples = [
    { title: 'Docker Container Initialized', description: 'MariaDB 11.2 instance running on port 3306' },
    { title: 'Go REST API Healthcheck', description: 'Endpoint /api/health returning status OK' },
    { title: 'Glassmorphism UI Rendered', description: 'Vanilla CSS stylesheet loaded with dynamic HSL themes' },
    { title: 'Database Migration Complete', description: 'Table `items` created with InnoDB engine' }
  ];

  seedBtn.addEventListener('click', () => {
    const randomSample = samples[Math.floor(Math.random() * samples.length)];
    itemTitle.value = randomSample.title;
    itemDesc.value = randomSample.description;
  });

  refreshBtn.addEventListener('click', () => {
    checkHealth();
    fetchItems();
  });

  // Initial Load
  checkHealth();
  fetchItems();

  // Periodic Health Check every 10 seconds
  setInterval(checkHealth, 10000);
});

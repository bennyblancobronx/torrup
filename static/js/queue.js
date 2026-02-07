// Queue page logic
// Requires: window.categoryOptions, window.csrfToken (set inline by template)

let currentFilter = 'all';
let autoRefreshInterval = null;
let queueData = [];

function csrfHeaders() {
  return window.csrfToken ? { 'X-CSRFToken': window.csrfToken } : {};
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text || '';
  return div.innerHTML;
}

function statusBadge(status) {
  const map = { queued: '', preparing: 'badge-info', uploading: 'badge-info', success: 'badge-success', failed: 'badge-error', duplicate: 'badge-warning' };
  return `<span class="badge ${map[escapeHtml(status)] || ''}">${escapeHtml(status)}</span>`;
}

function getActionsForStatus(status, id) {
  const actions = [];
  switch (status) {
    case 'queued':
      actions.push(`<button class="btn btn-ghost btn-sm" data-action="edit" data-id="${id}" title="Edit">E</button>`);
      actions.push(`<button class="btn btn-ghost btn-sm" data-action="delete" data-id="${id}" title="Delete">X</button>`);
      break;
    case 'preparing':
    case 'uploading':
      actions.push(`<button class="btn btn-ghost btn-sm" disabled title="In Progress">--</button>`);
      break;
    case 'success':
      actions.push(`<button class="btn btn-ghost btn-sm" data-action="view" data-id="${id}" title="View">V</button>`);
      break;
    case 'failed':
      actions.push(`<button class="btn btn-ghost btn-sm" data-action="retry" data-id="${id}" title="Retry">R</button>`);
      actions.push(`<button class="btn btn-ghost btn-sm" data-action="edit" data-id="${id}" title="Edit">E</button>`);
      actions.push(`<button class="btn btn-ghost btn-sm" data-action="delete" data-id="${id}" title="Delete">X</button>`);
      break;
    case 'duplicate':
      actions.push(`<button class="btn btn-ghost btn-sm" data-action="view" data-id="${id}" title="View">V</button>`);
      actions.push(`<button class="btn btn-ghost btn-sm" data-action="delete" data-id="${id}" title="Delete">X</button>`);
      break;
    default:
      actions.push(`<button class="btn btn-ghost btn-sm" data-action="view" data-id="${id}" title="View">V</button>`);
  }
  return actions.join('');
}

function filterQueue(data, filter) {
  if (filter === 'all') return data;
  if (filter === 'uploading') {
    return data.filter(item => item.status === 'uploading' || item.status === 'preparing');
  }
  return data.filter(item => item.status === filter);
}

function renderSummary(data) {
  const counts = { queued: 0, failed: 0, duplicate: 0, success: 0, preparing: 0, uploading: 0 };
  data.forEach(item => { if (counts[item.status] !== undefined) counts[item.status]++; });

  const parts = [];
  parts.push(`${data.length} total`);
  if (counts.queued) parts.push(`${counts.queued} queued`);
  if (counts.failed) parts.push(`${counts.failed} failed`);
  if (counts.duplicate) parts.push(`${counts.duplicate} duplicate`);
  if (counts.success) parts.push(`${counts.success} completed`);
  if (counts.uploading || counts.preparing) parts.push(`${counts.uploading + counts.preparing} in progress`);

  document.getElementById('queue-summary').textContent = parts.join(' | ');

  // Show/hide bulk buttons based on what exists
  document.getElementById('retry-all-btn').style.display = counts.failed > 0 ? '' : 'none';
  document.getElementById('clear-dupes-btn').style.display = counts.duplicate > 0 ? '' : 'none';
  document.getElementById('clear-completed-btn').style.display = counts.success > 0 ? '' : 'none';
}

function renderQueue(data) {
  renderSummary(data);
  const tbody = document.getElementById('queue-body');
  const filtered = filterQueue(data, currentFilter);

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="text-muted" style="text-align: center; padding: var(--space-6);">No items in queue</td></tr>`;
    return;
  }

  tbody.innerHTML = filtered.map(item => `
    <tr data-id="${item.id}">
      <td>${escapeHtml(String(item.id))}</td>
      <td>${escapeHtml(item.media_type)}</td>
      <td class="release-name" title="${escapeHtml(item.release_name)}">${escapeHtml(item.release_name)}</td>
      <td>${escapeHtml(String(item.category))}</td>
      <td>${statusBadge(item.status)}</td>
      <td class="text-sm text-muted" style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${escapeHtml(item.message || '')}">${escapeHtml(item.message || '')}</td>
      <td class="table-actions">${getActionsForStatus(item.status, item.id)}</td>
    </tr>
  `).join('');

  attachActionListeners();
}

function attachActionListeners() {
  document.querySelectorAll('[data-action]').forEach(btn => {
    btn.onclick = (e) => {
      const action = e.target.dataset.action;
      const id = parseInt(e.target.dataset.id, 10);
      handleAction(action, id);
    };
  });
}

function handleAction(action, id) {
  const item = queueData.find(i => i.id === id);
  if (!item) return;

  switch (action) {
    case 'edit':
      showEditPanel(item);
      break;
    case 'delete':
      deleteItem(id);
      break;
    case 'retry':
      retryItem(id);
      break;
    case 'view':
      showViewPanel(item);
      break;
  }
}

function showEditPanel(item) {
  const panel = document.getElementById('edit-panel');
  document.getElementById('edit-title').textContent = `Edit Item #${item.id}`;
  document.getElementById('edit-id').value = item.id;
  document.getElementById('edit-media-type').value = item.media_type;
  document.getElementById('edit-release-name').value = item.release_name;
  document.getElementById('edit-tags').value = item.tags || '';

  const imdbInput = document.getElementById('edit-imdb');
  const tvmazeidInput = document.getElementById('edit-tvmazeid');
  imdbInput.value = item.imdb || '';
  tvmazeidInput.value = item.tvmazeid || '';

  const metadataFields = document.getElementById('metadata-fields');
  if (item.media_type === 'movies' || item.media_type === 'tv') {
    metadataFields.style.display = 'grid';
  } else {
    metadataFields.style.display = 'none';
  }

  const categorySelect = document.getElementById('edit-category');
  const options = window.categoryOptions[item.media_type] || [];
  categorySelect.innerHTML = options.map(opt =>
    `<option value="${opt.id}" ${opt.id === item.category ? 'selected' : ''}>${escapeHtml(opt.label)}</option>`
  ).join('');

  panel.classList.add('visible');
}

function showViewPanel(item) {
  const panel = document.getElementById('edit-panel');
  document.getElementById('edit-title').textContent = `View Item #${item.id}`;
  document.getElementById('edit-id').value = item.id;
  document.getElementById('edit-media-type').value = item.media_type;
  document.getElementById('edit-release-name').value = item.release_name;
  document.getElementById('edit-release-name').disabled = true;
  document.getElementById('edit-tags').value = item.tags || '';
  document.getElementById('edit-tags').disabled = true;

  const categorySelect = document.getElementById('edit-category');
  const options = window.categoryOptions[item.media_type] || [];
  categorySelect.innerHTML = options.map(opt =>
    `<option value="${opt.id}" ${opt.id === item.category ? 'selected' : ''}>${escapeHtml(opt.label)}</option>`
  ).join('');
  categorySelect.disabled = true;

  document.getElementById('save-edit-btn').style.display = 'none';
  panel.classList.add('visible');
}

function hideEditPanel() {
  const panel = document.getElementById('edit-panel');
  panel.classList.remove('visible');
  document.getElementById('edit-release-name').disabled = false;
  document.getElementById('edit-tags').disabled = false;
  document.getElementById('edit-category').disabled = false;
  document.getElementById('save-edit-btn').style.display = '';
}

async function saveEdit() {
  const id = parseInt(document.getElementById('edit-id').value, 10);
  const releaseName = document.getElementById('edit-release-name').value;
  const category = document.getElementById('edit-category').value;
  const tags = document.getElementById('edit-tags').value;
  const imdb = document.getElementById('edit-imdb').value;
  const tvmazeid = document.getElementById('edit-tvmazeid').value;

  const res = await fetch('/api/queue/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() },
    body: JSON.stringify({ id, release_name: releaseName, category, tags, imdb, tvmazeid })
  });

  const data = await res.json();
  if (data.success) {
    hideEditPanel();
    await loadQueue();
  } else {
    alert(data.error || 'Failed to update item');
  }
}

async function deleteItem(id) {
  if (!confirm('Delete this item from the queue?')) return;

  const res = await fetch('/api/queue/delete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() },
    body: JSON.stringify({ id })
  });

  const data = await res.json();
  if (data.success) {
    await loadQueue();
  } else {
    alert(data.error || 'Failed to delete item');
  }
}

async function retryItem(id) {
  const res = await fetch('/api/queue/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() },
    body: JSON.stringify({ id, status: 'queued', message: '' })
  });

  const data = await res.json();
  if (data.success) {
    await loadQueue();
  } else {
    alert(data.error || 'Failed to retry item');
  }
}

async function retryAllFailed() {
  if (!confirm('Reset all failed items to queued?')) return;
  const res = await fetch('/api/queue/retry-all', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() }
  });
  const data = await res.json();
  if (data.success) await loadQueue();
  else alert(data.error || 'Failed');
}

async function clearDuplicates() {
  if (!confirm('Remove all duplicate items?')) return;
  const res = await fetch('/api/queue/clear-duplicates', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() }
  });
  const data = await res.json();
  if (data.success) await loadQueue();
  else alert(data.error || 'Failed');
}

async function clearCompleted() {
  if (!confirm('Remove all completed items?')) return;
  const res = await fetch('/api/queue/clear-completed', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() }
  });
  const data = await res.json();
  if (data.success) await loadQueue();
  else alert(data.error || 'Failed');
}

async function clearAll() {
  if (!confirm('Remove ALL items from the queue? This cannot be undone.')) return;
  const res = await fetch('/api/queue/clear-all', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() },
    body: JSON.stringify({ confirm: true })
  });
  const data = await res.json();
  if (data.success) await loadQueue();
  else alert(data.error || 'Failed');
}

async function loadQueue() {
  try {
    const res = await fetch('/api/queue');
    queueData = await res.json();
    renderQueue(queueData);
  } catch (err) {
    console.error('Failed to load queue:', err);
  }
}

function setFilter(filter) {
  currentFilter = filter;

  document.querySelectorAll('.filter-tabs .tab').forEach(btn => {
    btn.classList.toggle('is-active', btn.dataset.filter === filter);
  });

  document.getElementById('status-filter').value = filter;
  renderQueue(queueData);
}

function setupAutoRefresh() {
  const checkbox = document.getElementById('auto-refresh');

  if (checkbox.checked) {
    autoRefreshInterval = setInterval(loadQueue, 10000);
  }

  checkbox.onchange = () => {
    if (checkbox.checked) {
      autoRefreshInterval = setInterval(loadQueue, 10000);
    } else {
      clearInterval(autoRefreshInterval);
      autoRefreshInterval = null;
    }
  };
}

// Event listeners
document.querySelectorAll('.filter-tabs .tab').forEach(btn => {
  btn.onclick = () => setFilter(btn.dataset.filter);
});

document.getElementById('status-filter').onchange = (e) => {
  setFilter(e.target.value);
};

document.getElementById('refresh-btn').onclick = loadQueue;
document.getElementById('save-edit-btn').onclick = saveEdit;
document.getElementById('cancel-edit-btn').onclick = hideEditPanel;

document.getElementById('retry-all-btn').onclick = retryAllFailed;
document.getElementById('clear-dupes-btn').onclick = clearDuplicates;
document.getElementById('clear-completed-btn').onclick = clearCompleted;
document.getElementById('clear-all-btn').onclick = clearAll;

// Initialize
loadQueue();
setupAutoRefresh();

// Theme toggle
document.getElementById('theme-toggle').onclick = () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
};

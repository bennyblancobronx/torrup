// CSRF Token
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

// DOM Elements
const mediaTypeSelect = document.getElementById('media-type');
const refreshBtn = document.getElementById('refresh-btn');
const homeBtn = document.getElementById('home-btn');
const upBtn = document.getElementById('up-btn');
const breadcrumb = document.getElementById('breadcrumb');
const fileList = document.getElementById('file-list');
const selectAllCheckbox = document.getElementById('select-all');
const selectedCountEl = document.getElementById('selected-count');
const selectedSizeEl = document.getElementById('selected-size');
const addQueueBtn = document.getElementById('add-queue-btn');

// State
let currentPath = '';
let parentPath = null;
let currentDefaultCategory = null;
const selected = new Map();

// Helper: CSRF headers
function csrfHeaders() {
  return csrfToken ? { 'X-CSRFToken': csrfToken } : {};
}

// Helper: Escape HTML
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text || '';
  return div.innerHTML;
}

// Helper: Format bytes
function formatBytes(bytes) {
  if (bytes === 0 || bytes === null || bytes === undefined) return '--';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let i = 0;
  let size = bytes;
  while (size >= 1024 && i < units.length - 1) {
    size /= 1024;
    i++;
  }
  return size.toFixed(i === 0 ? 0 : 1) + ' ' + units[i];
}

// Update selection count and size
function updateSelectionSummary() {
  const count = selected.size;
  let totalSize = 0;
  for (const item of selected.values()) {
    if (item.size_bytes) {
      totalSize += item.size_bytes;
    }
  }
  selectedCountEl.textContent = count;
  selectedSizeEl.textContent = formatBytes(totalSize);
  addQueueBtn.disabled = count === 0;
}

// Clear all selections
function clearSelections() {
  selected.clear();
  selectAllCheckbox.checked = false;
  updateSelectionSummary();
}

// Render breadcrumb
function renderBreadcrumb(root, path) {
  breadcrumb.innerHTML = '';

  // Root segment
  const rootName = root ? root.split('/').pop() || root : 'Root';
  const rootSpan = document.createElement('span');
  rootSpan.className = 'breadcrumb-item';
  rootSpan.textContent = '/' + rootName;
  rootSpan.style.cursor = 'pointer';
  rootSpan.onclick = () => browse('');
  breadcrumb.appendChild(rootSpan);

  // Path segments
  if (path) {
    const segments = path.split('/').filter(Boolean);
    let accumulated = '';
    for (const segment of segments) {
      accumulated += '/' + segment;
      const sep = document.createElement('span');
      sep.className = 'breadcrumb-separator';
      sep.textContent = '>';
      breadcrumb.appendChild(sep);

      const segSpan = document.createElement('span');
      segSpan.className = 'breadcrumb-item';
      segSpan.textContent = segment;
      const segPath = accumulated;
      segSpan.style.cursor = 'pointer';
      segSpan.onclick = () => browse(segPath);
      breadcrumb.appendChild(segSpan);
    }
  }
}

// Browse directory
async function browse(path = '') {
  clearSelections();
  const mediaType = mediaTypeSelect.value;

  fileList.innerHTML = '<div class="loading-state">Loading...</div>';

  try {
    const response = await fetch(
      `/api/browse?media_type=${encodeURIComponent(mediaType)}&path=${encodeURIComponent(path)}`
    );
    const data = await response.json();

    if (data.error) {
      fileList.innerHTML = `<div class="empty-state">${escapeHtml(data.error)}</div>`;
      return;
    }

    currentPath = data.path || '';
    parentPath = data.parent || null;
    currentDefaultCategory = data.default_category || null;

    // Update breadcrumb
    renderBreadcrumb(data.root, data.path);

    // Update Up button state
    upBtn.disabled = !parentPath;

    // Render items
    if (!data.items || data.items.length === 0) {
      fileList.innerHTML = '<div class="empty-state">This folder is empty</div>';
      return;
    }

    fileList.innerHTML = '';
    for (const item of data.items) {
      const row = document.createElement('div');
      row.className = 'file-item';

      // Checkbox
      const checkboxCell = document.createElement('div');
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.dataset.path = item.path;
      checkbox.onchange = () => {
        if (checkbox.checked) {
          selected.set(item.path, item);
        } else {
          selected.delete(item.path);
        }
        updateSelectionSummary();
        updateSelectAllState();
      };
      checkboxCell.appendChild(checkbox);
      row.appendChild(checkboxCell);

      // Name with icon
      const nameCell = document.createElement('div');
      nameCell.className = 'file-name';

      const icon = document.createElement('span');
      icon.className = 'file-type-icon' + (item.is_dir ? ' is-folder' : '');
      icon.textContent = item.is_dir ? 'D' : 'F';
      nameCell.appendChild(icon);

      const nameText = document.createElement('span');
      nameText.className = 'file-name-text' + (item.is_dir ? ' is-folder' : '');
      nameText.textContent = item.name;
      nameText.title = item.path;
      if (item.is_dir) {
        nameText.onclick = () => browse(item.path);
      }
      nameCell.appendChild(nameText);
      row.appendChild(nameCell);

      // Size
      const sizeCell = document.createElement('div');
      sizeCell.className = 'file-size';
      sizeCell.textContent = item.is_dir ? '--' : formatBytes(item.size_bytes);
      row.appendChild(sizeCell);

      fileList.appendChild(row);
    }
  } catch (err) {
    console.error('Browse error:', err);
    fileList.innerHTML = '<div class="empty-state">Failed to load directory</div>';
  }
}

// Update select-all checkbox state
function updateSelectAllState() {
  const checkboxes = fileList.querySelectorAll('input[type="checkbox"]');
  if (checkboxes.length === 0) {
    selectAllCheckbox.checked = false;
    selectAllCheckbox.indeterminate = false;
    return;
  }
  const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
  if (checkedCount === 0) {
    selectAllCheckbox.checked = false;
    selectAllCheckbox.indeterminate = false;
  } else if (checkedCount === checkboxes.length) {
    selectAllCheckbox.checked = true;
    selectAllCheckbox.indeterminate = false;
  } else {
    selectAllCheckbox.checked = false;
    selectAllCheckbox.indeterminate = true;
  }
}

// Select all handler
selectAllCheckbox.onchange = () => {
  const checkboxes = fileList.querySelectorAll('input[type="checkbox"]');
  for (const checkbox of checkboxes) {
    checkbox.checked = selectAllCheckbox.checked;
    checkbox.dispatchEvent(new Event('change'));
  }
};

// Add to queue
async function addToQueue() {
  if (selected.size === 0) return;

  const mediaType = mediaTypeSelect.value;
  const items = Array.from(selected.values()).map(item => {
    const defaultCategory = currentDefaultCategory ||
      (categoryOptions[mediaType] && categoryOptions[mediaType][0]?.id);
    return {
      media_type: mediaType,
      path: item.path,
      category: defaultCategory
    };
  });

  addQueueBtn.disabled = true;
  addQueueBtn.textContent = 'Adding...';

  try {
    const res = await fetch('/api/queue/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...csrfHeaders()
      },
      body: JSON.stringify({ items })
    });
    const data = await res.json();

    if (data.success) {
      clearSelections();
      window.location.href = '/queue';
    } else {
      alert(data.error || 'Failed to add items to queue');
      addQueueBtn.disabled = false;
      addQueueBtn.textContent = 'Add to Queue';
    }
  } catch (err) {
    console.error('Add to queue error:', err);
    alert('Failed to add items to queue');
    addQueueBtn.disabled = false;
    addQueueBtn.textContent = 'Add to Queue';
  }
}

// Event listeners
mediaTypeSelect.onchange = () => browse('');
refreshBtn.onclick = () => browse(currentPath);
homeBtn.onclick = () => browse('');
upBtn.onclick = () => {
  if (parentPath !== null) {
    browse(parentPath);
  }
};
addQueueBtn.onclick = addToQueue;

// Initial load
browse('');

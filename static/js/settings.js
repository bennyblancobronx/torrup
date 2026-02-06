const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

function csrfHeaders() {
  return csrfToken ? { 'X-CSRFToken': csrfToken } : {};
}

async function saveSettings() {
  const data = {
    output_dir: document.getElementById('output_dir').value,
    release_group: document.getElementById('release_group').value,
    exclude_dirs: document.getElementById('exclude_dirs').value,
    test_mode: document.getElementById('test_mode').checked ? '1' : '0',
    extract_metadata: document.getElementById('extract_metadata').checked ? '1' : '0',
    extract_thumbnails: document.getElementById('extract_thumbnails').checked ? '1' : '0',
    enable_auto_upload: document.getElementById('enable_auto_upload').checked ? '1' : '0',
    auto_scan_interval: document.getElementById('auto_scan_interval').value,
    qbt_enabled: document.getElementById('qbt_enabled').checked ? '1' : '0',
    qbt_url: document.getElementById('qbt_url').value,
    qbt_user: document.getElementById('qbt_user').value,
    qbt_pass: document.getElementById('qbt_pass').value,
    tl_min_uploads_per_month: document.getElementById('tl_min_uploads_per_month').value,
    tl_min_seed_copies: document.getElementById('tl_min_seed_copies').value,
    tl_min_seed_days: document.getElementById('tl_min_seed_days').value,
    tl_inactivity_warning_weeks: document.getElementById('tl_inactivity_warning_weeks').value,
    tl_absence_notice_weeks: document.getElementById('tl_absence_notice_weeks').value,
    tl_enforce_activity: document.getElementById('tl_enforce_activity').checked ? '1' : '0',
    ntfy_enabled: document.getElementById('ntfy_enabled').checked ? '1' : '0',
    ntfy_url: document.getElementById('ntfy_url').value,
    ntfy_topic: document.getElementById('ntfy_topic').value,
    media_roots: [],
    templates: {},
  };

  document.querySelectorAll('#media-roots tbody tr').forEach(row => {
    const media_type = row.dataset.mediaType || row.children[0].textContent.trim();
    const enabled = row.querySelector('input[data-field="enabled"]').checked;
    const auto_scan = row.querySelector('input[data-field="auto_scan"]').checked;
    const path = row.querySelector('input[data-field="path"]').value;
    const default_category = row.querySelector('select[data-field="default_category"]').value;
    data.media_roots.push({ media_type, enabled, auto_scan, path, default_category });
  });

  document.querySelectorAll('input[data-template]').forEach(input => {
    data.templates[input.dataset.template] = input.value;
  });

  const res = await fetch('/api/settings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() },
    body: JSON.stringify(data),
  });
  const out = await res.json();
  const status = document.getElementById('status');
  status.textContent = out.success ? 'Saved' : (out.error || 'Save failed');
}

document.getElementById('save').onclick = saveSettings;

// Theme dropdown: set current value and apply on change
(function() {
  const sel = document.getElementById('theme_setting');
  sel.value = localStorage.getItem('theme') || 'system';
  sel.onchange = function() {
    const val = sel.value;
    localStorage.setItem('theme', val);
    if (val === 'system') {
      const sys = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', sys);
    } else {
      document.documentElement.setAttribute('data-theme', val);
    }
  };
})();

// Test qBT Connection
document.getElementById('test-qbt').onclick = async () => {
  const status = document.getElementById('qbt-test-status');
  status.textContent = 'Testing...';
  try {
    const res = await fetch('/api/settings/qbt/test', {
      method: 'POST',
      headers: { ...csrfHeaders() }
    });
    const out = await res.json();
    status.textContent = out.success ? `Connected! qBT version: ${out.version}` : `Error: ${out.error}`;
  } catch (e) {
    status.textContent = `Error: ${e.message}`;
  }
};

// --- Directory Picker ---
let dirPickerTarget = null;
let dirPickerCurrentPath = '/';

function openDirPicker(inputId) {
  dirPickerTarget = inputId;
  const currentVal = document.getElementById(inputId).value.trim();
  dirPickerCurrentPath = currentVal || '/';
  document.getElementById('dir-picker-backdrop').classList.remove('hidden');
  document.getElementById('dir-picker-modal').classList.remove('hidden');
  loadDirs(dirPickerCurrentPath);
}

function openDirPickerForRow(btn) {
  const input = btn.closest('.path-input-group').querySelector('input[data-field="path"]');
  dirPickerTarget = input;
  dirPickerCurrentPath = input.value.trim() || '/';
  document.getElementById('dir-picker-backdrop').classList.remove('hidden');
  document.getElementById('dir-picker-modal').classList.remove('hidden');
  loadDirs(dirPickerCurrentPath);
}

function closeDirPicker() {
  document.getElementById('dir-picker-backdrop').classList.add('hidden');
  document.getElementById('dir-picker-modal').classList.add('hidden');
  dirPickerTarget = null;
}

function selectDir() {
  if (dirPickerTarget) {
    const el = typeof dirPickerTarget === 'string'
      ? document.getElementById(dirPickerTarget)
      : dirPickerTarget;
    el.value = dirPickerCurrentPath;
  }
  closeDirPicker();
}

async function loadDirs(path) {
  const pathDisplay = document.getElementById('dir-current-path');
  const list = document.getElementById('dir-list');
  pathDisplay.textContent = path;
  list.innerHTML = '<li class="dir-empty">Loading...</li>';

  try {
    const res = await fetch('/api/browse-dirs?path=' + encodeURIComponent(path));
    const data = await res.json();
    if (!res.ok) {
      list.innerHTML = '<li class="dir-empty">' + (data.error || 'Failed to load') + '</li>';
      return;
    }
    dirPickerCurrentPath = data.path;
    pathDisplay.textContent = data.path;

    let html = '';
    if (data.parent) {
      html += '<li class="dir-item" onclick="loadDirs(\'' + escapeAttr(data.parent) + '\')">'
        + '<span class="dir-item-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg></span>'
        + '<span class="dir-item-name">..</span></li>';
    }
    for (const d of data.dirs) {
      html += '<li class="dir-item" onclick="loadDirs(\'' + escapeAttr(d.path) + '\')">'
        + '<span class="dir-item-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></span>'
        + '<span class="dir-item-name">' + escapeHtml(d.name) + '</span></li>';
    }
    if (!html) {
      html = '<li class="dir-empty">No subdirectories</li>';
    }
    list.innerHTML = html;
  } catch (e) {
    list.innerHTML = '<li class="dir-empty">Error: ' + escapeHtml(e.message) + '</li>';
  }
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function escapeAttr(str) {
  return str.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
}

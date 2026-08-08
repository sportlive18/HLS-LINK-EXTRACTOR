#!/usr/bin/env python3
"""
M3U Stream Extractor Pro 
Run: python m3u_extractor.py
Open: http://localhost:8080
No dependencies needed. Python 3.6+
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import sys

PORT = 8080

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>M3U Stream Extractor Pro</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {
  --primary: #6366f1;
  --primary-light: #818cf8;
  --primary-dark: #4f46e5;
  --success: #10b981;
  --danger: #ef4444;
  --bg: #f8fafc;
  --card: #ffffff;
  --text: #1e293b;
  --text-light: #64748b;
  --border: #e2e8f0;
  --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.05);
  --shadow-lg: 0 10px 40px rgba(99,102,241,0.15);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  padding: 20px;
  min-height: 100vh;
}
.container { max-width: 960px; margin: 0 auto; }

.header {
  text-align: center;
  margin-bottom: 32px;
  animation: fadeInDown 0.6s ease-out;
}
.header h1 {
  font-size: 32px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}
.header p { color: var(--text-light); font-size: 14px; }

.input-section {
  background: var(--card);
  border-radius: 20px;
  padding: 24px;
  box-shadow: var(--shadow);
  margin-bottom: 24px;
  animation: fadeInUp 0.6s ease-out 0.1s both;
  border: 1px solid var(--border);
}
.input-wrap { display: flex; gap: 12px; margin-bottom: 12px; }
.pro-input {
  flex: 1;
  padding: 14px 18px;
  border: 2px solid var(--border);
  border-radius: 14px;
  font-size: 14px;
  font-family: 'Inter', monospace;
  outline: none;
  transition: all 0.3s ease;
  background: #fafbfc;
}
.pro-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(99,102,241,0.1);
  background: white;
}
.pro-btn {
  padding: 14px 32px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  white-space: nowrap;
}
.pro-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s;
}
.pro-btn:hover::after { transform: translateX(100%); }
.pro-btn:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.pro-btn:active { transform: translateY(0) scale(0.98); }
.pro-btn:disabled { opacity: 0.7; cursor: not-allowed; transform: none !important; }
.quick-urls { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.quick-chip {
  padding: 6px 14px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  font-size: 11px;
  color: var(--text-light);
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}
.quick-chip:hover { background: var(--primary); color: white; border-color: var(--primary); transform: translateY(-1px); }

.stats-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  animation: fadeInUp 0.5s ease-out 0.2s both;
}
.stat-card {
  background: var(--card);
  padding: 16px 24px;
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  flex: 1;
  text-align: center;
  transition: all 0.3s ease;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-lg); }
.stat-num {
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.stat-label { font-size: 12px; color: var(--text-light); font-weight: 500; margin-top: 4px; }

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  animation: fadeInUp 0.5s ease-out 0.3s both;
  flex-wrap: wrap;
  gap: 10px;
}
.toolbar-left { display: flex; gap: 8px; flex-wrap: wrap; }
.toolbar-right { display: flex; gap: 8px; }
.tool-btn {
  padding: 8px 16px;
  background: white;
  border: 1.5px solid var(--border);
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text);
  cursor: pointer;
  transition: all 0.25s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}
.tool-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99,102,241,0.1);
}
.search-box {
  padding: 8px 14px;
  border: 1.5px solid var(--border);
  border-radius: 10px;
  font-size: 13px;
  outline: none;
  width: 200px;
  transition: all 0.3s;
}
.search-box:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
  width: 260px;
}

.channel-list { animation: fadeInUp 0.5s ease-out 0.4s both; }
.ch-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideIn 0.4s ease-out both;
  position: relative;
  overflow: hidden;
}
.ch-card::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, var(--primary), #a855f7);
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 16px 0 0 16px;
}
.ch-card:hover::before { opacity: 1; }
.ch-card:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-light);
}
.ch-logo-wrap { position: relative; flex-shrink: 0; }
.ch-logo {
  width: 52px; height: 52px;
  border-radius: 12px;
  object-fit: cover;
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  border: 2px solid var(--border);
  transition: all 0.3s;
}
.ch-card:hover .ch-logo { transform: scale(1.08); border-color: var(--primary-light); }
.ch-num {
  position: absolute;
  top: -6px; right: -6px;
  background: var(--primary);
  color: white;
  font-size: 9px;
  font-weight: 700;
  width: 20px; height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(99,102,241,0.4);
}
.ch-info { flex: 1; min-width: 0; }
.ch-name {
  font-size: 15px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.ch-meta { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.ch-group {
  font-size: 11px;
  font-weight: 600;
  background: linear-gradient(135deg, #ede9fe, #ddd6fe);
  color: var(--primary-dark);
  padding: 3px 10px;
  border-radius: 20px;
}
.ch-headers {
  font-size: 10px;
  color: var(--text-light);
  background: #f8fafc;
  padding: 2px 8px;
  border-radius: 6px;
  border: 1px solid var(--border);
}
.ch-url-box {
  margin-top: 8px;
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 8px 12px;
  font-size: 11px;
  font-family: 'SF Mono', monospace;
  color: var(--text-light);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: text;
  transition: all 0.2s;
}
.ch-url-box:hover { background: #f1f5f9; border-color: var(--primary-light); }
.ch-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;
}
.act-btn {
  width: 36px; height: 36px;
  border-radius: 10px;
  border: 1.5px solid var(--border);
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}
.act-btn:hover {
  transform: scale(1.12) rotate(4deg);
  border-color: var(--primary);
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  box-shadow: 0 4px 12px rgba(99,102,241,0.3);
}
.act-btn svg { transition: all 0.2s; }
.act-btn:hover svg { stroke: white; }
.act-btn.copied {
  background: var(--success);
  border-color: var(--success);
  color: white;
  animation: pop 0.4s ease;
}
.act-btn.copied svg { stroke: white; }

.empty-state {
  text-align: center;
  padding: 80px 20px;
  animation: fadeIn 0.8s ease;
}
.empty-orb {
  width: 80px; height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #ede9fe, #ddd6fe);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: float 3s ease-in-out infinite;
}
.empty-state h3 { font-size: 18px; color: var(--text); margin-bottom: 6px; }
.empty-state p { color: var(--text-light); font-size: 14px; }

.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}
.toast {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  color: white;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  transform: translateX(120%);
  opacity: 0;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 10px;
  pointer-events: auto;
  border-left: 3px solid var(--success);
}
.toast.show { transform: translateX(0); opacity: 1; }
.toast.error { border-left-color: var(--danger); }
.toast-icon { font-size: 16px; }

.loading-overlay {
  position: fixed;
  inset: 0;
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(8px);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 999;
  flex-direction: column;
  gap: 16px;
}
.loading-overlay.active { display: flex; }
.loader {
  width: 48px; height: 48px;
  border: 3px solid #e2e8f0;
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
.loader-text { color: var(--text-light); font-size: 14px; font-weight: 500; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
@keyframes pop { 0% { transform: scale(1); } 50% { transform: scale(1.2); } 100% { transform: scale(1); } }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 640px) {
  .input-wrap { flex-direction: column; }
  .stats-bar { flex-direction: column; }
  .toolbar { flex-direction: column; align-items: stretch; }
  .ch-card { flex-wrap: wrap; }
  .ch-actions { flex-direction: row; width: 100%; justify-content: flex-end; }
}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🔴 M3U Stream Extractor Pro</h1>
    <p>Fetch, parse & copy every stream URL with style</p>
  </div>

  <div class="input-section">
    <div class="input-wrap">
      <input type="text" id="m3uUrl" class="pro-input" 
        placeholder="https://raw.githubusercontent.com/.../playlist.m3u"
        value="https://raw.githubusercontent.com/sportlive18/Hotstar-Auto-Update/refs/heads/main/playlist.m3u">
      <button id="scanBtn" class="pro-btn" onclick="scanM3U()">
        <span id="btnText">🔍 Scan M3U</span>
      </button>
    </div>
    <div class="quick-urls">
      <span style="font-size:11px;color:var(--text-light);margin-right:4px;">Quick:</span>
      <span class="quick-chip" onclick="setUrl('https://raw.githubusercontent.com/sportlive18/Hotstar-Auto-Update/refs/heads/main/playlist.m3u')">Hotstar Playlist</span>
      <span class="quick-chip" onclick="setUrl('https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in.m3u')">IPTV India</span>
      <span class="quick-chip" onclick="setUrl('https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8')">Free-TV Global</span>
    </div>
  </div>

  <div id="resultsArea" style="display:none;">
    <div class="stats-bar">
      <div class="stat-card">
        <div class="stat-num" id="totalChannels">0</div>
        <div class="stat-label">Channels</div>
      </div>
      <div class="stat-card">
        <div class="stat-num" id="totalGroups">0</div>
        <div class="stat-label">Groups</div>
      </div>
      <div class="stat-card">
        <div class="stat-num" id="totalUrls">0</div>
        <div class="stat-label">Stream URLs</div>
      </div>
    </div>

    <div class="toolbar">
      <div class="toolbar-left">
        <button class="tool-btn" onclick="copyAllUrls()">📋 Copy All URLs</button>
        <button class="tool-btn" onclick="copyAllWithHeaders()">🔗 Copy All + Headers</button>
        <button class="tool-btn" onclick="copyAsJson()">📦 Copy as JSON</button>
        <button class="tool-btn" onclick="copyAsCurl()">🖥️ Copy as cURL</button>
        <button class="tool-btn" onclick="downloadM3U()">💾 Download M3U</button>
      </div>
      <div class="toolbar-right">
        <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search channels..." oninput="filterChannels()">
      </div>
    </div>

    <div class="channel-list" id="channelsList"></div>
  </div>

  <div id="emptyState" class="empty-state">
    <div class="empty-orb">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2">
        <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
      </svg>
    </div>
    <h3>Ready to Extract</h3>
    <p>Paste a GitHub raw M3U URL and hit Scan to begin</p>
  </div>
</div>

<div class="loading-overlay" id="loader">
  <div class="loader"></div>
  <div class="loader-text">Fetching playlist...</div>
</div>

<div class="toast-container" id="toastContainer"></div>

<script>
let parsedChannels = [];
let filteredChannels = [];

function setUrl(url) {
  document.getElementById('m3uUrl').value = url;
  document.getElementById('m3uUrl').focus();
}

function showToast(msg, type) {
  type = type || 'success';
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = 'toast ' + type;
  toast.innerHTML = '<span class="toast-icon">' + (type === 'success' ? '✅' : '❌') + '</span><span>' + msg + '</span>';
  container.appendChild(toast);
  requestAnimationFrame(function() { toast.classList.add('show'); });
  setTimeout(function() {
    toast.classList.remove('show');
    setTimeout(function() { toast.remove(); }, 400);
  }, 2500);
}

async function scanM3U() {
  const url = document.getElementById('m3uUrl').value.trim();
  const btn = document.getElementById('scanBtn');
  const btnText = document.getElementById('btnText');
  if (!url) { showToast('Please enter a URL', 'error'); return; }

  btn.disabled = true;
  btnText.textContent = 'Scanning...';
  document.getElementById('loader').classList.add('active');

  try {
    const res = await fetch('/api/fetch?url=' + encodeURIComponent(url));
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const text = await res.text();
    parseM3U(text);
    showToast('Found ' + parsedChannels.length + ' channels!');
  } catch (e) {
    showToast('Failed: ' + e.message, 'error');
  } finally {
    btn.disabled = false;
    btnText.textContent = '🔍 Scan M3U';
    document.getElementById('loader').classList.remove('active');
  }
}

function parseM3U(text) {
  const lines = text.split(/\r?\n/);
  parsedChannels = [];
  let current = { name: '', group: '', logo: '', url: '', headers: {}, rawLines: [] };
  const groups = new Set();

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;
    current.rawLines.push(line);

    if (line.startsWith('#EXTINF:')) {
      const nameMatch = line.match(/,\s*(.+)$/);
      current.name = nameMatch ? nameMatch[1].trim() : 'Unknown Channel';
      const groupMatch = line.match(/group-title="([^"]+)"/);
      current.group = groupMatch ? groupMatch[1] : 'Uncategorized';
      const logoMatch = line.match(/tvg-logo="([^"]+)"/);
      current.logo = logoMatch ? logoMatch[1] : '';
      const nameAttr = line.match(/tvg-name="([^"]+)"/);
      if (nameAttr && current.name === 'Unknown Channel') current.name = nameAttr[1];
    }
    else if (line.startsWith('#EXTVLCOPT:')) {
      const opt = line.replace('#EXTVLCOPT:', '').trim();
      if (opt.startsWith('http-user-agent=')) current.headers['User-Agent'] = opt.substring(16);
      if (opt.startsWith('http-referrer=')) current.headers['Referer'] = opt.substring(14);
      if (opt.startsWith('http-cookie=')) current.headers['Cookie'] = opt.substring(12);
      if (opt.startsWith('http-origin=')) current.headers['Origin'] = opt.substring(12);
    }
    else if (line.startsWith('#EXTHTTP:')) {
      try { Object.assign(current.headers, JSON.parse(line.replace('#EXTHTTP:', '').trim())); } catch(e) {}
    }
    else if (line.startsWith('http')) {
      current.url = line;
      parsedChannels.push(Object.assign({}, current, { id: parsedChannels.length + 1 }));
      groups.add(current.group);
      current = { name: '', group: '', logo: '', url: '', headers: {}, rawLines: [] };
    }
  }

  filteredChannels = parsedChannels.slice();
  renderResults(groups);
}

function renderResults(groups) {
  document.getElementById('emptyState').style.display = 'none';
  document.getElementById('resultsArea').style.display = 'block';
  document.getElementById('totalChannels').textContent = parsedChannels.length;
  document.getElementById('totalGroups').textContent = groups.size;
  document.getElementById('totalUrls').textContent = parsedChannels.length;
  renderChannelList();
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function renderChannelList() {
  const list = document.getElementById('channelsList');
  if (filteredChannels.length === 0) {
    list.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-light);">No channels match your search.</div>';
    return;
  }
  list.innerHTML = filteredChannels.map(function(ch, idx) {
    const headerTags = Object.keys(ch.headers).length > 0 
      ? Object.keys(ch.headers).map(function(k) { return k.substring(0,3); }).join(', ') 
      : 'No headers';
    const delay = (idx % 10) * 0.05;
    return '<div class="ch-card" style="animation-delay:' + delay + 's">' +
      '<div class="ch-logo-wrap">' +
        '<img class="ch-logo" src="' + (ch.logo || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(ch.name) + '&background=6366f1&color=fff&size=128') + '" ' +
             'onerror="this.src=\'https://ui-avatars.com/api/?name=' + encodeURIComponent(ch.name) + '&background=6366f1&color=fff&size=128\'" alt="">' +
        '<span class="ch-num">' + ch.id + '</span>' +
      '</div>' +
      '<div class="ch-info">' +
        '<div class="ch-name">' + escapeHtml(ch.name) + '</div>' +
        '<div class="ch-meta">' +
          '<span class="ch-group">' + escapeHtml(ch.group) + '</span>' +
          '<span class="ch-headers">' + headerTags + '</span>' +
        '</div>' +
        '<div class="ch-url-box" title="' + escapeHtml(ch.url) + '">' + escapeHtml(ch.url) + '</div>' +
      '</div>' +
      '<div class="ch-actions">' +
        '<button class="act-btn" title="Copy URL" onclick="copyUrl(' + ch.id + ', this)">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>' +
          '</svg>' +
        '</button>' +
        '<button class="act-btn" title="Copy URL + Headers" onclick="copyWithHeaders(' + ch.id + ', this)">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/>' +
          '</svg>' +
        '</button>' +
        '<button class="act-btn" title="Copy as cURL" onclick="copyCurl(' + ch.id + ', this)">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>' +
          '</svg>' +
        '</button>' +
        '<button class="act-btn" title="Copy as JSON" onclick="copyJson(' + ch.id + ', this)">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>' +
          '</svg>' +
        '</button>' +
        '<button class="act-btn" title="Play in VLC" onclick="playVlc(' + ch.id + ')">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<polygon points="5 3 19 12 5 21 5 3"/>' +
          '</svg>' +
        '</button>' +
      '</div>' +
    '</div>';
  }).join('');
}

function getChannelById(id) {
  for (var i = 0; i < parsedChannels.length; i++) {
    if (parsedChannels[i].id === id) return parsedChannels[i];
  }
  return null;
}

function animateCopy(btn) {
  btn.classList.add('copied');
  setTimeout(function() { btn.classList.remove('copied'); }, 1200);
}

function copyUrl(id, btn) {
  var ch = getChannelById(id);
  navigator.clipboard.writeText(ch.url).then(function() {
    animateCopy(btn);
    showToast('Copied: ' + ch.name.substring(0, 20) + '...');
  });
}

function copyWithHeaders(id, btn) {
  var ch = getChannelById(id);
  var text = ch.url;
  if (ch.headers['User-Agent']) text += '\nUser-Agent: ' + ch.headers['User-Agent'];
  if (ch.headers['Referer']) text += '\nReferer: ' + ch.headers['Referer'];
  if (ch.headers['Cookie']) text += '\nCookie: ' + ch.headers['Cookie'];
  if (ch.headers['Origin']) text += '\nOrigin: ' + ch.headers['Origin'];
  navigator.clipboard.writeText(text).then(function() {
    animateCopy(btn);
    showToast('URL + Headers copied!');
  });
}

function copyCurl(id, btn) {
  var ch = getChannelById(id);
  var cmd = 'curl -L "' + ch.url + '"';
  if (ch.headers['User-Agent']) cmd += ' -H "User-Agent: ' + ch.headers['User-Agent'] + '"';
  if (ch.headers['Referer']) cmd += ' -H "Referer: ' + ch.headers['Referer'] + '"';
  if (ch.headers['Cookie']) cmd += ' -H "Cookie: ' + ch.headers['Cookie'] + '"';
  if (ch.headers['Origin']) cmd += ' -H "Origin: ' + ch.headers['Origin'] + '"';
  navigator.clipboard.writeText(cmd).then(function() {
    animateCopy(btn);
    showToast('cURL command copied!');
  });
}

function copyJson(id, btn) {
  var ch = getChannelById(id);
  var json = JSON.stringify({
    name: ch.name,
    group: ch.group,
    logo: ch.logo,
    url: ch.url,
    headers: ch.headers
  }, null, 2);
  navigator.clipboard.writeText(json).then(function() {
    animateCopy(btn);
    showToast('JSON copied!');
  });
}

function playVlc(id) {
  var ch = getChannelById(id);
  window.open('vlc://' + ch.url, '_blank');
}

function copyAllUrls() {
  var urls = parsedChannels.map(function(c) { return c.url; }).join('\n');
  navigator.clipboard.writeText(urls).then(function() {
    showToast('Copied ' + parsedChannels.length + ' URLs!');
  });
}

function copyAllWithHeaders() {
  var text = parsedChannels.map(function(c) {
    var s = c.url;
    if (c.headers['User-Agent']) s += '\n  User-Agent: ' + c.headers['User-Agent'];
    if (c.headers['Referer']) s += '\n  Referer: ' + c.headers['Referer'];
    if (c.headers['Cookie']) s += '\n  Cookie: ' + c.headers['Cookie'];
    return s;
  }).join('\n\n---\n\n');
  navigator.clipboard.writeText(text).then(function() {
    showToast('All URLs + Headers copied!');
  });
}

function copyAsJson() {
  var json = JSON.stringify(parsedChannels, null, 2);
  navigator.clipboard.writeText(json).then(function() {
    showToast('Full JSON copied!');
  });
}

function copyAsCurl() {
  var cmds = parsedChannels.map(function(c) {
    var cmd = 'curl -L "' + c.url + '"';
    if (c.headers['User-Agent']) cmd += ' -H "User-Agent: ' + c.headers['User-Agent'] + '"';
    if (c.headers['Referer']) cmd += ' -H "Referer: ' + c.headers['Referer'] + '"';
    if (c.headers['Cookie']) cmd += ' -H "Cookie: ' + c.headers['Cookie'] + '"';
    return '# ' + c.name + '\n' + cmd;
  }).join('\n\n');
  navigator.clipboard.writeText(cmds).then(function() {
    showToast('All cURL commands copied!');
  });
}

function downloadM3U() {
  var content = '#EXTM3U\n';
  for (var i = 0; i < parsedChannels.length; i++) {
    var ch = parsedChannels[i];
    content += '#EXTINF:-1 tvg-name="' + ch.name + '" group-title="' + ch.group + '"' + (ch.logo ? ' tvg-logo="' + ch.logo + '"' : '') + ',' + ch.name + '\n';
    if (ch.headers['User-Agent']) content += '#EXTVLCOPT:http-user-agent=' + ch.headers['User-Agent'] + '\n';
    if (ch.headers['Referer']) content += '#EXTVLCOPT:http-referrer=' + ch.headers['Referer'] + '\n';
    if (ch.headers['Cookie']) content += '#EXTVLCOPT:http-cookie=' + ch.headers['Cookie'] + '\n';
    if (ch.headers['Origin']) content += '#EXTVLCOPT:http-origin=' + ch.headers['Origin'] + '\n';
    content += ch.url + '\n';
  }
  var blob = new Blob([content], {type: 'audio/x-mpegurl'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'extracted_playlist.m3u';
  document.body.appendChild(a);
  a.click();
  a.remove();
  showToast('M3U downloaded!');
}

function filterChannels() {
  var q = document.getElementById('searchBox').value.toLowerCase();
  filteredChannels = parsedChannels.filter(function(c) {
    return c.name.toLowerCase().includes(q) || 
           c.group.toLowerCase().includes(q) ||
           c.url.toLowerCase().includes(q);
  });
  renderChannelList();
}

document.getElementById('m3uUrl').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') scanM3U();
});
</script>
</body>
</html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress logs

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)

        if parsed.path == '/api/fetch':
            url = query.get('url', [''])[0]
            if not url:
                self.send_error(400, 'Missing URL')
                return
            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Accept': '*/*'
                    }
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            return

        # Serve the main page
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 55)
        print("  M3U Stream Extractor Pro")
        print("=" * 55)
        print(f"  Open http://localhost:{PORT} in your browser")
        print("  Press Ctrl+C to stop")
        print("=" * 55)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Server stopped.")
            sys.exit(0)

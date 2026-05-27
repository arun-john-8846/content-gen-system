/* app.js — UI helpers for ADAP Content Gen Web */

// ── Research log polling ──────────────────────────────────────────────────────

function startLogPolling(slug) {
  var offset = 0;
  var captchaShown = false;
  var intervalId = null;

  function poll() {
    fetch('/pages/' + slug + '/research/log?since=' + offset)
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (data.text) {
          var el = document.getElementById('log-output');
          if (el) {
            el.textContent += data.text;
            el.scrollTop = el.scrollHeight;
          }
          offset = data.offset;
        }

        if (data.captcha && !captchaShown) {
          captchaShown = true;
          var banner = document.getElementById('captcha-banner');
          if (banner) banner.style.display = 'block';
        }

        var badge = document.getElementById('log-status-badge');
        if (badge) {
          badge.textContent = data.status.charAt(0).toUpperCase() + data.status.slice(1);
          badge.className = 'badge badge-' + (
            data.status === 'running' ? 'running' :
            data.status === 'done'    ? 'pass'    : 'fail'
          );
        }

        if (data.status === 'done' || data.status === 'error') {
          clearInterval(intervalId);
          if (data.status === 'done') {
            setTimeout(function() { window.location.reload(); }, 1500);
          }
        }
      })
      .catch(function(err) { console.error('Log poll error:', err); });
  }

  intervalId = setInterval(poll, 1000);
  poll();
}

function sendCaptchaContinue() {
  var slug = window.location.pathname.split('/')[2];
  fetch('/pages/' + slug + '/research/captcha-continue', { method: 'POST' })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      var banner = document.getElementById('captcha-banner');
      if (banner) {
        banner.innerHTML = data.ok
          ? '<strong>Signal sent.</strong> Research is continuing — watch the log above.'
          : '<strong>Could not send signal.</strong> Switch to the Terminal and press Enter there.';
      }
    })
    .catch(function() {
      var banner = document.getElementById('captcha-banner');
      if (banner) banner.innerHTML = '<strong>Error.</strong> Switch to the Terminal and press Enter there.';
    });
}


// ── Pipeline SSE stream ───────────────────────────────────────────────────────

function startPipelineStream(slug, isRunning) {
  var logEl = document.getElementById('pipeline-log');
  var badge = document.getElementById('pipeline-status-badge');

  function setBadge(running) {
    if (!badge) return;
    badge.textContent = running ? 'Running' : 'Idle';
    badge.className = 'badge ' + (running ? 'badge-running' : 'badge-pass');
  }

  // Load existing log lines first via polling endpoint (handles page refresh)
  function loadExisting(cb) {
    fetch('/pages/' + slug + '/pipeline/status?offset=0')
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (logEl && data.lines && data.lines.length) {
          logEl.textContent = data.lines.join('\n');
          logEl.scrollTop = logEl.scrollHeight;
        }
        cb(data.offset);
      })
      .catch(function() { cb(0); });
  }

  if (!isRunning) {
    // Just show existing log, no live stream needed
    loadExisting(function() {});
    return;
  }

  // Active pipeline — open SSE stream
  var evtSource = new EventSource('/pages/' + slug + '/pipeline/stream');
  setBadge(true);

  evtSource.onmessage = function(e) {
    var msg = e.data;

    if (msg === '__DONE__' || msg === '__TIMEOUT__') {
      evtSource.close();
      setBadge(false);
      // Reload page after a brief pause so step progress refreshes
      setTimeout(function() { window.location.reload(); }, 1500);
      return;
    }

    try {
      var line = JSON.parse(msg);
      if (logEl) {
        logEl.textContent += (logEl.textContent ? '\n' : '') + line;
        logEl.scrollTop = logEl.scrollHeight;
      }
    } catch(err) {
      // not JSON — just append raw
      if (logEl) {
        logEl.textContent += '\n' + msg;
        logEl.scrollTop = logEl.scrollHeight;
      }
    }
  };

  evtSource.onerror = function() {
    evtSource.close();
    setBadge(false);
  };
}


// ── Flash message auto-dismiss ────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.flash').forEach(function(el) {
    setTimeout(function() {
      el.style.transition = 'opacity .5s';
      el.style.opacity = '0';
      setTimeout(function() { el.remove(); }, 500);
    }, 5000);
  });
});

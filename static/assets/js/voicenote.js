/* Notes vocales — enregistreur (MediaRecorder) + lecteur, partagé par les chats. */
window.VoiceNote = (function () {
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function fmtDur(s) { s = Math.round(s || 0); return Math.floor(s / 60) + ':' + pad(s % 60); }

  // ── Lecteur (délégation de clic sur un conteneur) ──
  function initPlayers(root, sel) {
    let current = null;
    root.addEventListener('click', function (e) {
      const btn = e.target.closest(sel + ' .vn-play');
      if (!btn) return;
      const box = btn.closest(sel);
      const prog = box.querySelector('.vn-prog');
      const time = box.querySelector('.vn-time');
      const dur = parseInt(box.dataset.dur || '0', 10);
      let audio = box._audio;
      if (!audio) {
        audio = new Audio(box.dataset.src);
        box._audio = audio;
        audio.addEventListener('timeupdate', function () {
          const d = (audio.duration && isFinite(audio.duration)) ? audio.duration : dur;
          if (d && prog) prog.style.width = (audio.currentTime / d * 100) + '%';
          if (time) time.textContent = fmtDur(audio.currentTime);
        });
        audio.addEventListener('ended', function () {
          btn.textContent = '▶'; if (prog) prog.style.width = '0%'; if (time) time.textContent = fmtDur(dur);
        });
      }
      if (audio.paused) {
        if (current && current !== audio) { current.pause(); const b = current._btn; if (b) b.textContent = '▶'; }
        current = audio; audio._btn = btn; audio.play(); btn.textContent = '⏸';
      } else {
        audio.pause(); btn.textContent = '▶';
      }
    });
  }

  function chooseMime() {
    const prefs = ['audio/mp4', 'audio/webm;codecs=opus', 'audio/webm', 'audio/ogg'];
    for (let i = 0; i < prefs.length; i++) {
      if (window.MediaRecorder && MediaRecorder.isTypeSupported(prefs[i])) return prefs[i];
    }
    return '';
  }

  // ── Enregistreur ──
  // opts : micBtn, bar (conteneur d'enregistrement), timer, cancelBtn, sendBtn, onSend(blob, seconds, filename)
  function attachRecorder(opts) {
    let rec = null, chunks = [], stream = null, startTs = 0, timerInt = null, secs = 0;
    const mime = chooseMime();

    function showBar(on) { if (opts.bar) opts.bar.classList.toggle('rec-on', on); }
    function tick() {
      secs = Math.round((Date.now() - startTs) / 1000);
      if (opts.timer) opts.timer.textContent = fmtDur(secs);
      if (secs >= 125) stop(true);           // garde-fou ~2 min
    }
    function cleanup() {
      clearInterval(timerInt);
      if (stream) { stream.getTracks().forEach(function (t) { t.stop(); }); }
      stream = null; showBar(false);
    }
    async function start() {
      if (!navigator.mediaDevices || !window.MediaRecorder) {
        alert("L'enregistrement audio n'est pas supporté par ce navigateur."); return;
      }
      try { stream = await navigator.mediaDevices.getUserMedia({ audio: true }); }
      catch (e) { alert('Accès au micro refusé ou indisponible.'); return; }
      chunks = []; secs = 0;
      try { rec = new MediaRecorder(stream, mime ? { mimeType: mime } : undefined); }
      catch (e) { rec = new MediaRecorder(stream); }
      rec.ondataavailable = function (e) { if (e.data && e.data.size) chunks.push(e.data); };
      rec.start();
      startTs = Date.now(); if (opts.timer) opts.timer.textContent = '0:00';
      showBar(true); timerInt = setInterval(tick, 250);
    }
    function stop(send) {
      if (!rec) { cleanup(); return; }
      const finalSecs = secs;
      rec.onstop = function () {
        cleanup();
        if (send && chunks.length) {
          const type = rec.mimeType || mime || 'audio/webm';
          const blob = new Blob(chunks, { type: type });
          let ext = 'webm';
          if (type.indexOf('mp4') >= 0) ext = 'm4a';
          else if (type.indexOf('ogg') >= 0) ext = 'ogg';
          opts.onSend(blob, finalSecs || 1, 'note.' + ext);
        }
        rec = null; chunks = [];
      };
      try { rec.stop(); } catch (e) { cleanup(); rec = null; }
    }

    if (opts.micBtn)    opts.micBtn.addEventListener('click', start);
    if (opts.cancelBtn) opts.cancelBtn.addEventListener('click', function () { stop(false); });
    if (opts.sendBtn)   opts.sendBtn.addEventListener('click', function () { stop(true); });
  }

  return { initPlayers: initPlayers, attachRecorder: attachRecorder, fmtDur: fmtDur };
})();

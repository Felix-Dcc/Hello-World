// Small extras on top of pages that already work without JavaScript.
(function () {
  'use strict';

  // One submission per page: a second click or keypress before the next page
  // arrives would race the first, and both carry the same session cookie.
  document.querySelectorAll('form[method=post]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (form.dataset.busy) { e.preventDefault(); return; }
      form.dataset.busy = '1';
    });
  });
  // Coming Back to a page from the back/forward cache: make its forms usable again.
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) document.querySelectorAll('form[data-busy]').forEach(function (f) { delete f.dataset.busy; });
  });

  // Hangman: type letters on the physical keyboard.
  var board = document.querySelector('[data-hangman]');
  if (board) {
    document.addEventListener('keydown', function (e) {
      if (e.ctrlKey || e.metaKey || e.altKey || !/^[a-z]$/i.test(e.key)) return;
      var key = board.querySelector('button[data-letter="' + e.key.toLowerCase() + '"]');
      if (key && !key.disabled) key.click();
    });
  }

  // Copy-to-clipboard buttons (hidden until we know they can work).
  document.querySelectorAll('[data-copy]').forEach(function (button) {
    var target = document.querySelector(button.getAttribute('data-copy'));
    if (!target || !navigator.clipboard) return;
    button.hidden = false;
    button.addEventListener('click', function () {
      navigator.clipboard.writeText(target.value).then(function () {
        button.textContent = 'Copied!';
        setTimeout(function () { button.textContent = 'Copy'; }, 1500);
      });
    });
  });

  // Range inputs: show the live value, and submit when let go.
  document.querySelectorAll('form[data-autosubmit]').forEach(function (form) {
    form.querySelectorAll('[data-hide-with-js]').forEach(function (el) { el.hidden = true; });
    form.querySelectorAll('input[type=range]').forEach(function (input) {
      var out = form.querySelector('[data-output-for="' + input.id + '"]');
      input.addEventListener('input', function () { if (out) out.textContent = input.value; });
      input.addEventListener('change', function () { form.submit(); });
    });
  });
})();

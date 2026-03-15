/* Cryptosites.com — Application JavaScript */
(function() {
  'use strict';

  /* Theme management (in-memory only) */
  var currentTheme = 'dark';

  function applyTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
  }

  applyTheme(currentTheme);

  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function(e) {
    applyTheme(e.matches ? 'light' : 'dark');
  });

  /* Starred platforms (in-memory) */
  var starredPlatforms = [];

  function updateStarredUI() {
    var countEl = document.getElementById('starredCount');
    var listEl = document.getElementById('starredList');
    if (!countEl || !listEl) return;

    var count = starredPlatforms.length;
    countEl.textContent = count;
    countEl.style.display = count > 0 ? 'flex' : 'none';

    if (count === 0) {
      listEl.innerHTML = '<div class="starred-dropdown-empty">Star a platform to track it here</div>';
    } else {
      listEl.innerHTML = starredPlatforms.map(function(p) {
        return '<a href="' + p.url + '" class="starred-dropdown-item"><span>' + p.name + '</span><span style="font-size:12px;color:var(--text-muted)">' + p.category + '</span></a>';
      }).join('');
    }
  }

  function toggleStar(name, url, category) {
    var idx = starredPlatforms.findIndex(function(p) { return p.name === name; });
    if (idx >= 0) {
      starredPlatforms.splice(idx, 1);
    } else {
      starredPlatforms.push({ name: name, url: url, category: category });
    }
    updateStarredUI();
    var starBtn = document.getElementById('starBrandBtn');
    if (starBtn) {
      var isStarred = starredPlatforms.some(function(p) { return p.name === name; });
      starBtn.classList.toggle('is-starred', isStarred);
      starBtn.querySelector('span').textContent = isStarred ? 'Starred' : 'Star';
    }
  }

  /* Make toggleStar available globally */
  window.toggleStar = toggleStar;

  /* DOM ready */
  document.addEventListener('DOMContentLoaded', function() {

    /* Theme toggle */
    var themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', function() {
        applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
      });
    }

    /* Mobile menu toggle */
    var mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    var mobileNav = document.querySelector('.mobile-nav');
    if (mobileMenuBtn && mobileNav) {
      mobileMenuBtn.addEventListener('click', function() {
        var isOpen = mobileNav.classList.toggle('is-open');
        mobileMenuBtn.setAttribute('aria-expanded', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
      });
      mobileNav.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function() {
          mobileNav.classList.remove('is-open');
          mobileMenuBtn.setAttribute('aria-expanded', 'false');
          document.body.style.overflow = '';
        });
      });
    }

    /* Starred badge dropdown */
    var starredBadge = document.getElementById('starredBadge');
    if (starredBadge) {
      starredBadge.addEventListener('click', function(e) {
        e.stopPropagation();
        starredBadge.classList.toggle('open');
      });
      document.addEventListener('click', function() {
        starredBadge.classList.remove('open');
      });
    }
    updateStarredUI();

    /* FAQ accordion (original) */
    var faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(function(item) {
      var question = item.querySelector('.faq-question');
      if (question) {
        question.addEventListener('click', function() {
          var wasOpen = item.classList.contains('is-open');
          faqItems.forEach(function(i) { i.classList.remove('is-open'); });
          if (!wasOpen) item.classList.add('is-open');
        });
      }
    });

    /* Comparison table sorting */
    var tables = document.querySelectorAll('.comparison-table');
    tables.forEach(function(table) {
      var headers = table.querySelectorAll('th[data-sort]');
      headers.forEach(function(header) {
        header.addEventListener('click', function() {
          var sortKey = header.getAttribute('data-sort');
          var tbody = table.querySelector('tbody');
          var rows = Array.from(tbody.querySelectorAll('tr'));
          var isNumeric = header.hasAttribute('data-numeric');
          var currentDir = header.getAttribute('data-dir') || 'asc';
          var newDir = currentDir === 'asc' ? 'desc' : 'asc';
          headers.forEach(function(h) { h.removeAttribute('data-dir'); });
          header.setAttribute('data-dir', newDir);
          rows.sort(function(a, b) {
            var aVal = a.querySelector('[data-' + sortKey + ']')?.getAttribute('data-' + sortKey) || a.cells[header.cellIndex]?.textContent.trim() || '';
            var bVal = b.querySelector('[data-' + sortKey + ']')?.getAttribute('data-' + sortKey) || b.cells[header.cellIndex]?.textContent.trim() || '';
            var comparison;
            if (isNumeric) { comparison = parseFloat(aVal) - parseFloat(bVal); }
            else { comparison = aVal.localeCompare(bVal); }
            return newDir === 'asc' ? comparison : -comparison;
          });
          rows.forEach(function(row) { tbody.appendChild(row); });
        });
      });
    });

    /* Scroll animation */
    var observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);
    document.querySelectorAll('.observe-animate').forEach(function(el) {
      observer.observe(el);
    });

    /* Newsletter form */
    var newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(function(form) {
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        var input = form.querySelector('input[type="email"]');
        var btn = form.querySelector('.btn');
        if (input && input.value) {
          btn.textContent = 'Subscribed!';
          btn.style.background = 'var(--success)';
          input.value = '';
          setTimeout(function() {
            btn.textContent = 'Subscribe';
            btn.style.background = '';
          }, 3000);
        }
      });
    });

  });
})();

/* Copy promo code to clipboard */
function copyCode(btn, code) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(code).then(function() {
      btn.textContent = 'Copied!';
      btn.style.background = 'var(--success)';
      setTimeout(function() {
        btn.textContent = 'Copy';
        btn.style.background = '';
      }, 2000);
    });
  } else {
    var textarea = document.createElement('textarea');
    textarea.value = code;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    btn.textContent = 'Copied!';
    btn.style.background = 'var(--success)';
    setTimeout(function() {
      btn.textContent = 'Copy';
      btn.style.background = '';
    }, 2000);
  }
}

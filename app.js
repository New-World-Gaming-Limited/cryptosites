/* ============================================
   Cryptosites.com — Application JavaScript
   ============================================ */

(function() {
  'use strict';

  // Theme management (in-memory only)
  // Default to dark mode; only switch to light if user explicitly toggles
  let currentTheme = 'dark';

  function applyTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
  }

  // Apply initial theme
  applyTheme(currentTheme);

  // Listen for system theme changes
  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function(e) {
    applyTheme(e.matches ? 'light' : 'dark');
  });

  // DOM ready
  document.addEventListener('DOMContentLoaded', function() {

    // Theme toggle
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', function() {
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
      });
    }

    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mobileNav = document.querySelector('.mobile-nav');
    if (mobileMenuBtn && mobileNav) {
      mobileMenuBtn.addEventListener('click', function() {
        const isOpen = mobileNav.classList.toggle('is-open');
        mobileMenuBtn.setAttribute('aria-expanded', isOpen);
        // Prevent body scroll when menu is open
        document.body.style.overflow = isOpen ? 'hidden' : '';
      });

      // Close mobile nav on link click
      mobileNav.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function() {
          mobileNav.classList.remove('is-open');
          mobileMenuBtn.setAttribute('aria-expanded', 'false');
          document.body.style.overflow = '';
        });
      });
    }

    // FAQ accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(function(item) {
      const question = item.querySelector('.faq-question');
      if (question) {
        question.addEventListener('click', function() {
          const wasOpen = item.classList.contains('is-open');
          // Close all FAQ items
          faqItems.forEach(function(i) { i.classList.remove('is-open'); });
          // Toggle the clicked one
          if (!wasOpen) {
            item.classList.add('is-open');
          }
        });
      }
    });

    // Comparison table sorting
    const tables = document.querySelectorAll('.comparison-table');
    tables.forEach(function(table) {
      const headers = table.querySelectorAll('th[data-sort]');
      headers.forEach(function(header) {
        header.addEventListener('click', function() {
          const sortKey = header.getAttribute('data-sort');
          const tbody = table.querySelector('tbody');
          const rows = Array.from(tbody.querySelectorAll('tr'));
          const isNumeric = header.hasAttribute('data-numeric');
          const currentDir = header.getAttribute('data-dir') || 'asc';
          const newDir = currentDir === 'asc' ? 'desc' : 'asc';

          // Reset all headers
          headers.forEach(function(h) { h.removeAttribute('data-dir'); });
          header.setAttribute('data-dir', newDir);

          rows.sort(function(a, b) {
            const aVal = a.querySelector('[data-' + sortKey + ']')?.getAttribute('data-' + sortKey) || a.cells[header.cellIndex]?.textContent.trim() || '';
            const bVal = b.querySelector('[data-' + sortKey + ']')?.getAttribute('data-' + sortKey) || b.cells[header.cellIndex]?.textContent.trim() || '';

            let comparison;
            if (isNumeric) {
              comparison = parseFloat(aVal) - parseFloat(bVal);
            } else {
              comparison = aVal.localeCompare(bVal);
            }
            return newDir === 'asc' ? comparison : -comparison;
          });

          rows.forEach(function(row) { tbody.appendChild(row); });
        });
      });
    });

    // Scroll animation (IntersectionObserver)
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };
    const observer = new IntersectionObserver(function(entries) {
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

    // Newsletter form handling
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(function(form) {
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        const input = form.querySelector('input[type="email"]');
        const btn = form.querySelector('.btn');
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

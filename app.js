/* ==========================================================================
   CryptoBets.com — Application JavaScript
   Complete interactive functionality for the crypto betting affiliate site.
   Uses in-memory state only (sandboxed iframe restriction).
   ========================================================================== */

(function () {
  'use strict';

  /* --------------------------------------------------------------------------
     § 1. THEME TOGGLE
     Dark/light mode with system preference detection.
     -------------------------------------------------------------------------- */

  const ThemeManager = {
    // In-memory store
    currentTheme: null,

    init() {
      const toggle = document.querySelector('[data-theme-toggle]');
      const html = document.documentElement;

      // Detect system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
      this.currentTheme = prefersDark.matches ? 'dark' : 'light';

      // Apply initial theme
      html.setAttribute('data-theme', this.currentTheme);
      this.updateToggleIcon(toggle);

      // Listen for toggle clicks
      if (toggle) {
        toggle.addEventListener('click', () => {
          this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
          html.setAttribute('data-theme', this.currentTheme);
          this.updateToggleIcon(toggle);
        });
      }

      // Listen for system preference changes
      prefersDark.addEventListener('change', (e) => {
        // Only auto-switch if user hasn't manually toggled
        // (We can't persist this, so we always follow system on reload)
        this.currentTheme = e.matches ? 'dark' : 'light';
        html.setAttribute('data-theme', this.currentTheme);
        this.updateToggleIcon(toggle);
      });
    },

    updateToggleIcon(toggle) {
      if (!toggle) return;
      const isDark = this.currentTheme === 'dark';
      toggle.setAttribute('aria-label', `Switch to ${isDark ? 'light' : 'dark'} mode`);
      toggle.innerHTML = isDark
        ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
        : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    }
  };


  /* --------------------------------------------------------------------------
     § 2. MOBILE MENU
     Slide-out menu with body scroll lock.
     -------------------------------------------------------------------------- */

  const MobileMenu = {
    isOpen: false,
    scrollPosition: 0,

    init() {
      const btn = document.querySelector('[data-mobile-menu-btn]');
      const menu = document.querySelector('[data-mobile-menu]');
      const overlay = document.querySelector('[data-mobile-overlay]');

      if (!btn || !menu) return;

      btn.addEventListener('click', () => {
        this.isOpen ? this.close(btn, menu, overlay) : this.open(btn, menu, overlay);
      });

      // Close on overlay click
      if (overlay) {
        overlay.addEventListener('click', () => {
          this.close(btn, menu, overlay);
        });
      }

      // Close on Escape
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.isOpen) {
          this.close(btn, menu, overlay);
        }
      });

      // Handle submenu toggles within mobile menu
      const submenuToggles = menu.querySelectorAll('[data-submenu-toggle]');
      submenuToggles.forEach((toggle) => {
        toggle.addEventListener('click', (e) => {
          e.preventDefault();
          const target = toggle.getAttribute('data-submenu-toggle');
          const submenu = menu.querySelector(`[data-submenu="${target}"]`);
          if (submenu) {
            submenu.classList.toggle('mobile-menu__submenu--open');
            toggle.setAttribute('aria-expanded',
              submenu.classList.contains('mobile-menu__submenu--open'));
          }
        });
      });
    },

    open(btn, menu, overlay) {
      this.isOpen = true;
      this.scrollPosition = window.scrollY;
      btn.setAttribute('aria-expanded', 'true');
      menu.classList.add('mobile-menu--open');
      if (overlay) overlay.classList.add('mobile-menu__overlay--visible');
      document.body.classList.add('body-scroll-lock');
      document.body.style.top = `-${this.scrollPosition}px`;
    },

    close(btn, menu, overlay) {
      this.isOpen = false;
      btn.setAttribute('aria-expanded', 'false');
      menu.classList.remove('mobile-menu--open');
      if (overlay) overlay.classList.remove('mobile-menu__overlay--visible');
      document.body.classList.remove('body-scroll-lock');
      document.body.style.top = '';
      window.scrollTo(0, this.scrollPosition);
    }
  };


  /* --------------------------------------------------------------------------
     § 3. SMOOTH SCROLL FOR ANCHOR LINKS
     -------------------------------------------------------------------------- */

  const SmoothScroll = {
    init() {
      document.addEventListener('click', (e) => {
        const link = e.target.closest('a[href^="#"]');
        if (!link) return;

        const targetId = link.getAttribute('href');
        if (targetId === '#') return;

        const target = document.querySelector(targetId);
        if (!target) return;

        e.preventDefault();

        const headerHeight = document.querySelector('.site-header')?.offsetHeight || 0;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight - 20;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });

        // Update URL hash without jumping
        if (history.pushState) {
          history.pushState(null, null, targetId);
        }
      });
    }
  };


  /* --------------------------------------------------------------------------
     § 4. COPY TO CLIPBOARD (Promo Codes)
     -------------------------------------------------------------------------- */

  const CopyToClipboard = {
    init() {
      document.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-copy]');
        if (!btn) return;

        const targetSelector = btn.getAttribute('data-copy');
        const target = document.querySelector(targetSelector);
        const text = target ? target.textContent.trim() : btn.textContent.trim();

        this.copy(text, btn);
      });
    },

    async copy(text, btn) {
      try {
        await navigator.clipboard.writeText(text);
        this.showSuccess(btn);
      } catch {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand('copy');
          this.showSuccess(btn);
        } catch {
          // Silent fail
        }
        document.body.removeChild(textarea);
      }
    },

    showSuccess(btn) {
      const promoCode = btn.closest('.promo-code');
      const originalHTML = btn.innerHTML;
      const originalText = btn.textContent;

      // Add copied state
      if (promoCode) {
        promoCode.classList.add('promo-code--copied');
      }

      btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg> Copied!';

      // Show toast
      ToastManager.show('Promo code copied!', 'success');

      // Reset after 2 seconds
      setTimeout(() => {
        btn.innerHTML = originalHTML;
        if (promoCode) {
          promoCode.classList.remove('promo-code--copied');
        }
      }, 2000);
    }
  };


  /* --------------------------------------------------------------------------
     § 5. FAQ ACCORDION
     -------------------------------------------------------------------------- */

  const FAQAccordion = {
    init() {
      const triggers = document.querySelectorAll('[data-faq-trigger]');

      triggers.forEach((trigger) => {
        trigger.addEventListener('click', () => {
          const item = trigger.closest('.faq-item');
          if (!item) return;

          const isOpen = item.classList.contains('faq-item--open');

          // Optional: close all others (single-open mode)
          if (trigger.hasAttribute('data-faq-single')) {
            const siblings = item.parentElement.querySelectorAll('.faq-item--open');
            siblings.forEach((sib) => {
              if (sib !== item) {
                sib.classList.remove('faq-item--open');
                const sibTrigger = sib.querySelector('[data-faq-trigger]');
                if (sibTrigger) sibTrigger.setAttribute('aria-expanded', 'false');
              }
            });
          }

          item.classList.toggle('faq-item--open');
          trigger.setAttribute('aria-expanded', !isOpen);
        });
      });

      // Also handle generic details/summary based accordions
      const termsTriggers = document.querySelectorAll('[data-terms-trigger]');
      termsTriggers.forEach((trigger) => {
        trigger.addEventListener('click', () => {
          const terms = trigger.closest('.promo-terms');
          if (terms) {
            terms.classList.toggle('promo-terms--open');
          }
        });
      });
    }
  };


  /* --------------------------------------------------------------------------
     § 6. SEARCH OVERLAY
     -------------------------------------------------------------------------- */

  const SearchOverlay = {
    init() {
      const openBtns = document.querySelectorAll('[data-search-open]');
      const overlay = document.querySelector('[data-search-overlay]');
      const closeBtn = overlay?.querySelector('[data-search-close]');
      const input = overlay?.querySelector('[data-search-input]');

      if (!overlay) return;

      openBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          this.open(overlay, input);
        });
      });

      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          this.close(overlay);
        });
      }

      // Close on backdrop click
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          this.close(overlay);
        }
      });

      // Close on Escape
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && overlay.classList.contains('search-overlay--open')) {
          this.close(overlay);
        }
      });

      // Keyboard shortcut: Cmd/Ctrl + K
      document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
          e.preventDefault();
          if (overlay.classList.contains('search-overlay--open')) {
            this.close(overlay);
          } else {
            this.open(overlay, input);
          }
        }
      });

      // Handle search input
      if (input) {
        input.addEventListener('input', debounce((e) => {
          this.handleSearch(e.target.value, overlay);
        }, 300));
      }
    },

    open(overlay, input) {
      overlay.classList.add('search-overlay--open');
      document.body.classList.add('body-scroll-lock');
      if (input) {
        setTimeout(() => input.focus(), 100);
      }
    },

    close(overlay) {
      overlay.classList.remove('search-overlay--open');
      document.body.classList.remove('body-scroll-lock');
    },

    handleSearch(query, overlay) {
      const results = overlay.querySelector('[data-search-results]');
      const empty = overlay.querySelector('[data-search-empty]');
      if (!results) return;

      // This is a placeholder — in production, this would hit an API
      if (query.length < 2) {
        results.innerHTML = '';
        if (empty) empty.style.display = 'block';
        return;
      }

      if (empty) empty.style.display = 'none';
      // Placeholder results rendering would go here
    }
  };


  /* --------------------------------------------------------------------------
     § 7. SCROLL-AWARE HEADER
     Hide on scroll down, show on scroll up.
     -------------------------------------------------------------------------- */

  const ScrollHeader = {
    lastScrollY: 0,
    ticking: false,
    threshold: 60,

    init() {
      const header = document.querySelector('.site-header');
      if (!header) return;

      window.addEventListener('scroll', () => {
        if (!this.ticking) {
          requestAnimationFrame(() => {
            this.update(header);
            this.ticking = false;
          });
          this.ticking = true;
        }
      }, { passive: true });
    },

    update(header) {
      const currentScrollY = window.scrollY;

      // Add scrolled state
      if (currentScrollY > 10) {
        header.classList.add('site-header--scrolled');
      } else {
        header.classList.remove('site-header--scrolled');
      }

      // Hide/show based on direction
      if (currentScrollY > this.lastScrollY && currentScrollY > this.threshold) {
        // Scrolling down — hide
        header.classList.add('site-header--hidden');
      } else {
        // Scrolling up — show
        header.classList.remove('site-header--hidden');
      }

      this.lastScrollY = currentScrollY;
    }
  };


  /* --------------------------------------------------------------------------
     § 8. INTERSECTION OBSERVER — Fade-in Animations
     -------------------------------------------------------------------------- */

  const ScrollAnimations = {
    init() {
      // Check for reduced motion preference
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

      const animatedElements = document.querySelectorAll(
        '.fade-in, .slide-up, .slide-left, .slide-right, .scale-in, .stagger'
      );

      if (animatedElements.length === 0) return;

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              const el = entry.target;
              const classes = el.classList;

              if (classes.contains('fade-in'))      classes.add('fade-in--visible');
              if (classes.contains('slide-up'))      classes.add('slide-up--visible');
              if (classes.contains('slide-left'))    classes.add('slide-left--visible');
              if (classes.contains('slide-right'))   classes.add('slide-right--visible');
              if (classes.contains('scale-in'))      classes.add('scale-in--visible');
              if (classes.contains('stagger'))       classes.add('stagger--visible');

              observer.unobserve(el);
            }
          });
        },
        {
          threshold: 0.1,
          rootMargin: '0px 0px -50px 0px'
        }
      );

      animatedElements.forEach((el) => observer.observe(el));
    }
  };


  /* --------------------------------------------------------------------------
     § 9. COMPARISON TABLE FILTERS
     -------------------------------------------------------------------------- */

  const TableFilters = {
    init() {
      const filterBars = document.querySelectorAll('[data-table-filter]');

      filterBars.forEach((bar) => {
        const tableId = bar.getAttribute('data-table-filter');
        const table = document.getElementById(tableId);
        if (!table) return;

        const tags = bar.querySelectorAll('.tag');

        tags.forEach((tag) => {
          tag.addEventListener('click', () => {
            // Update active state
            tags.forEach((t) => t.classList.remove('tag--active'));
            tag.classList.add('tag--active');

            const filter = tag.getAttribute('data-filter');
            this.filterTable(table, filter);
          });
        });
      });
    },

    filterTable(table, filter) {
      const rows = table.querySelectorAll('tbody tr');

      rows.forEach((row) => {
        if (filter === 'all') {
          row.style.display = '';
          return;
        }

        const categories = row.getAttribute('data-categories') || '';
        if (categories.includes(filter)) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    }
  };


  /* --------------------------------------------------------------------------
     § 10. BONUS BROWSER CAROUSEL
     -------------------------------------------------------------------------- */

  const BonusCarousel = {
    carousels: [],

    init() {
      const containers = document.querySelectorAll('[data-carousel]');

      containers.forEach((container) => {
        const track = container.querySelector('[data-carousel-track]');
        const prevBtn = container.querySelector('[data-carousel-prev]');
        const nextBtn = container.querySelector('[data-carousel-next]');
        const dotsContainer = container.querySelector('[data-carousel-dots]');

        if (!track) return;

        const slides = track.children;
        const state = {
          currentIndex: 0,
          totalSlides: slides.length,
          slidesPerView: this.getSlidesPerView(),
          track,
          prevBtn,
          nextBtn,
          dotsContainer,
          slides
        };

        this.carousels.push(state);
        this.buildDots(state);
        this.updateCarousel(state);

        if (prevBtn) {
          prevBtn.addEventListener('click', () => {
            state.currentIndex = Math.max(0, state.currentIndex - 1);
            this.updateCarousel(state);
          });
        }

        if (nextBtn) {
          nextBtn.addEventListener('click', () => {
            const maxIndex = state.totalSlides - state.slidesPerView;
            state.currentIndex = Math.min(maxIndex, state.currentIndex + 1);
            this.updateCarousel(state);
          });
        }

        // Touch/swipe support
        let startX = 0;
        let isDragging = false;

        track.addEventListener('touchstart', (e) => {
          startX = e.touches[0].clientX;
          isDragging = true;
        }, { passive: true });

        track.addEventListener('touchend', (e) => {
          if (!isDragging) return;
          isDragging = false;
          const endX = e.changedTouches[0].clientX;
          const diff = startX - endX;

          if (Math.abs(diff) > 50) {
            if (diff > 0) {
              // Swipe left — next
              const maxIndex = state.totalSlides - state.slidesPerView;
              state.currentIndex = Math.min(maxIndex, state.currentIndex + 1);
            } else {
              // Swipe right — prev
              state.currentIndex = Math.max(0, state.currentIndex - 1);
            }
            this.updateCarousel(state);
          }
        }, { passive: true });
      });

      // Update on resize
      window.addEventListener('resize', debounce(() => {
        const newPerView = this.getSlidesPerView();
        this.carousels.forEach((state) => {
          state.slidesPerView = newPerView;
          state.currentIndex = Math.min(
            state.currentIndex,
            Math.max(0, state.totalSlides - state.slidesPerView)
          );
          this.buildDots(state);
          this.updateCarousel(state);
        });
      }, 200));
    },

    getSlidesPerView() {
      if (window.innerWidth >= 1024) return 3;
      if (window.innerWidth >= 768) return 2;
      return 1;
    },

    buildDots(state) {
      if (!state.dotsContainer) return;
      state.dotsContainer.innerHTML = '';
      const totalDots = Math.max(1, state.totalSlides - state.slidesPerView + 1);
      for (let i = 0; i < totalDots; i++) {
        const dot = document.createElement('button');
        dot.className = 'bonus-browser__dot';
        dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
        dot.addEventListener('click', () => {
          state.currentIndex = i;
          this.updateCarousel(state);
        });
        state.dotsContainer.appendChild(dot);
      }
    },

    updateCarousel(state) {
      const slideWidth = 100 / state.slidesPerView;
      const offset = -(state.currentIndex * slideWidth);
      state.track.style.transform = `translateX(${offset}%)`;

      // Update buttons
      if (state.prevBtn) {
        state.prevBtn.disabled = state.currentIndex <= 0;
      }
      if (state.nextBtn) {
        state.nextBtn.disabled = state.currentIndex >= state.totalSlides - state.slidesPerView;
      }

      // Update dots
      if (state.dotsContainer) {
        const dots = state.dotsContainer.querySelectorAll('.bonus-browser__dot');
        dots.forEach((dot, i) => {
          dot.classList.toggle('bonus-browser__dot--active', i === state.currentIndex);
        });
      }
    }
  };


  /* --------------------------------------------------------------------------
     § 11. QUIZ STEPPER
     Multi-step platform matching quiz logic.
     -------------------------------------------------------------------------- */

  const QuizStepper = {
    quizzes: [],

    init() {
      const quizContainers = document.querySelectorAll('[data-quiz]');

      quizContainers.forEach((container) => {
        const steps = container.querySelectorAll('[data-quiz-step]');
        const progressSteps = container.querySelectorAll('.quiz__progress-step');
        const nextBtn = container.querySelector('[data-quiz-next]');
        const prevBtn = container.querySelector('[data-quiz-prev]');
        const resultsPanel = container.querySelector('[data-quiz-results]');

        const state = {
          currentStep: 0,
          totalSteps: steps.length,
          answers: {},
          steps,
          progressSteps,
          nextBtn,
          prevBtn,
          resultsPanel,
          container
        };

        this.quizzes.push(state);

        // Option selection
        container.addEventListener('click', (e) => {
          const option = e.target.closest('.quiz__option');
          if (!option) return;

          const stepEl = option.closest('[data-quiz-step]');
          if (!stepEl) return;

          // Deselect siblings
          stepEl.querySelectorAll('.quiz__option').forEach((opt) => {
            opt.classList.remove('quiz__option--selected');
          });

          // Select this one
          option.classList.add('quiz__option--selected');
          state.answers[state.currentStep] = option.getAttribute('data-value');

          // Enable next button
          if (state.nextBtn) state.nextBtn.disabled = false;
        });

        // Navigation
        if (nextBtn) {
          nextBtn.addEventListener('click', () => {
            if (state.currentStep < state.totalSteps - 1) {
              state.currentStep++;
              this.updateQuiz(state);
            } else {
              this.showResults(state);
            }
          });
        }

        if (prevBtn) {
          prevBtn.addEventListener('click', () => {
            if (state.currentStep > 0) {
              state.currentStep--;
              this.updateQuiz(state);
            }
          });
        }

        // Initialize
        this.updateQuiz(state);
      });
    },

    updateQuiz(state) {
      // Show/hide steps
      state.steps.forEach((step, i) => {
        step.style.display = i === state.currentStep ? 'block' : 'none';
      });

      // Update progress
      state.progressSteps.forEach((step, i) => {
        step.classList.remove('quiz__progress-step--active', 'quiz__progress-step--completed');
        if (i < state.currentStep) {
          step.classList.add('quiz__progress-step--completed');
        } else if (i === state.currentStep) {
          step.classList.add('quiz__progress-step--active');
        }
      });

      // Update buttons
      if (state.prevBtn) {
        state.prevBtn.style.display = state.currentStep > 0 ? 'inline-flex' : 'none';
      }

      if (state.nextBtn) {
        state.nextBtn.textContent = state.currentStep === state.totalSteps - 1
          ? 'See Results'
          : 'Next';
        state.nextBtn.disabled = !state.answers[state.currentStep];
      }
    },

    showResults(state) {
      // Hide all steps
      state.steps.forEach((step) => { step.style.display = 'none'; });

      // Show results
      if (state.resultsPanel) {
        state.resultsPanel.style.display = 'block';
      }

      // Mark all progress as completed
      state.progressSteps.forEach((step) => {
        step.classList.remove('quiz__progress-step--active');
        step.classList.add('quiz__progress-step--completed');
      });

      // Hide navigation
      if (state.nextBtn) state.nextBtn.style.display = 'none';
      if (state.prevBtn) state.prevBtn.style.display = 'none';
    }
  };


  /* --------------------------------------------------------------------------
     § 12. COUNT-UP ANIMATION ON SCROLL
     Animates numbers from 0 to their target value when scrolled into view.
     -------------------------------------------------------------------------- */

  const CountUp = {
    init() {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

      const elements = document.querySelectorAll('[data-count-up]');
      if (elements.length === 0) return;

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              this.animate(entry.target);
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.5 }
      );

      elements.forEach((el) => observer.observe(el));
    },

    animate(el) {
      const target = parseFloat(el.getAttribute('data-count-up'));
      const duration = parseInt(el.getAttribute('data-count-duration') || '1500', 10);
      const decimals = parseInt(el.getAttribute('data-count-decimals') || '0', 10);
      const prefix = el.getAttribute('data-count-prefix') || '';
      const suffix = el.getAttribute('data-count-suffix') || '';

      const start = performance.now();

      const step = (now) => {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);

        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = target * eased;

        el.textContent = prefix + current.toFixed(decimals) + suffix;

        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          el.textContent = prefix + target.toFixed(decimals) + suffix;
        }
      };

      requestAnimationFrame(step);
    }
  };


  /* --------------------------------------------------------------------------
     § 13. TABLE OF CONTENTS — Highlight on Scroll
     -------------------------------------------------------------------------- */

  const TableOfContents = {
    init() {
      const toc = document.querySelector('[data-toc]');
      if (!toc) return;

      const links = toc.querySelectorAll('.toc__link');
      const sections = [];

      links.forEach((link) => {
        const href = link.getAttribute('href');
        if (!href || href === '#') return;
        const section = document.querySelector(href);
        if (section) {
          sections.push({ link, section });
        }
      });

      if (sections.length === 0) return;

      const headerOffset = 100;

      const update = () => {
        const scrollY = window.scrollY + headerOffset;

        let activeSection = sections[0];

        for (const item of sections) {
          if (item.section.offsetTop <= scrollY) {
            activeSection = item;
          }
        }

        links.forEach((link) => link.classList.remove('toc__link--active'));
        if (activeSection) {
          activeSection.link.classList.add('toc__link--active');
        }
      };

      window.addEventListener('scroll', () => {
        requestAnimationFrame(update);
      }, { passive: true });

      // Initial call
      update();
    }
  };


  /* --------------------------------------------------------------------------
     § 14. BACK TO TOP BUTTON
     -------------------------------------------------------------------------- */

  const BackToTop = {
    init() {
      const btn = document.querySelector('[data-back-to-top]');
      if (!btn) return;

      const showThreshold = 400;

      window.addEventListener('scroll', () => {
        requestAnimationFrame(() => {
          if (window.scrollY > showThreshold) {
            btn.classList.add('back-to-top--visible');
          } else {
            btn.classList.remove('back-to-top--visible');
          }
        });
      }, { passive: true });

      btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }
  };


  /* --------------------------------------------------------------------------
     § 15. TOAST NOTIFICATIONS
     In-memory notification system.
     -------------------------------------------------------------------------- */

  const ToastManager = {
    container: null,

    init() {
      // Create container if it doesn't exist
      this.container = document.querySelector('.toast-container');
      if (!this.container) {
        this.container = document.createElement('div');
        this.container.className = 'toast-container';
        this.container.setAttribute('aria-live', 'polite');
        document.body.appendChild(this.container);
      }
    },

    show(message, type = 'info', duration = 3000) {
      if (!this.container) this.init();

      const toast = document.createElement('div');
      toast.className = `toast toast--${type}`;

      const iconMap = {
        success: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>',
        error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/></svg>',
        info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>'
      };

      toast.innerHTML = `
        <span class="toast__icon">${iconMap[type] || iconMap.info}</span>
        <div class="toast__content">
          <p class="toast__message">${message}</p>
        </div>
        <button class="toast__close" aria-label="Close notification">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
      `;

      // Close button
      toast.querySelector('.toast__close').addEventListener('click', () => {
        this.dismiss(toast);
      });

      this.container.appendChild(toast);

      // Auto-dismiss
      if (duration > 0) {
        setTimeout(() => this.dismiss(toast), duration);
      }
    },

    dismiss(toast) {
      toast.classList.add('toast--leaving');
      setTimeout(() => {
        toast.remove();
      }, 300);
    }
  };


  /* --------------------------------------------------------------------------
     § 16. TABS COMPONENT
     -------------------------------------------------------------------------- */

  const TabsComponent = {
    init() {
      const tabGroups = document.querySelectorAll('[data-tabs]');

      tabGroups.forEach((group) => {
        const tabs = group.querySelectorAll('.tabs__tab');
        const panels = group.querySelectorAll('.tabs__panel');

        tabs.forEach((tab) => {
          tab.addEventListener('click', () => {
            const targetId = tab.getAttribute('data-tab');

            // Deactivate all
            tabs.forEach((t) => t.classList.remove('tabs__tab--active'));
            panels.forEach((p) => p.classList.remove('tabs__panel--active'));

            // Activate clicked
            tab.classList.add('tabs__tab--active');
            const targetPanel = group.querySelector(`[data-tab-panel="${targetId}"]`);
            if (targetPanel) targetPanel.classList.add('tabs__panel--active');
          });
        });
      });
    }
  };


  /* --------------------------------------------------------------------------
     § 17. SCORING BARS ANIMATION
     Animate width on scroll into view.
     -------------------------------------------------------------------------- */

  const ScoringBars = {
    init() {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

      const bars = document.querySelectorAll('[data-score-width]');
      if (bars.length === 0) return;

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              const width = entry.target.getAttribute('data-score-width');
              entry.target.style.width = width + '%';
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.3 }
      );

      bars.forEach((bar) => observer.observe(bar));
    }
  };


  /* --------------------------------------------------------------------------
     § 18. RATING WHEEL ANIMATION
     -------------------------------------------------------------------------- */

  const RatingWheel = {
    init() {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

      const wheels = document.querySelectorAll('[data-rating-wheel]');
      if (wheels.length === 0) return;

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              const fill = entry.target.querySelector('.rating-wheel__fill');
              const rating = parseFloat(entry.target.getAttribute('data-rating-wheel'));
              if (fill) {
                const circumference = 226; // 2 * PI * 36
                const offset = circumference - (rating / 10) * circumference;
                fill.style.strokeDashoffset = offset;
              }
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.5 }
      );

      wheels.forEach((wheel) => observer.observe(wheel));
    }
  };


  /* --------------------------------------------------------------------------
     § 19. LIGHTBOX (Screenshot Gallery)
     -------------------------------------------------------------------------- */

  const Lightbox = {
    currentIndex: 0,
    images: [],

    init() {
      const galleries = document.querySelectorAll('[data-gallery]');

      galleries.forEach((gallery) => {
        const items = gallery.querySelectorAll('[data-lightbox-src]');

        items.forEach((item, index) => {
          item.addEventListener('click', () => {
            this.images = Array.from(items).map((i) => i.getAttribute('data-lightbox-src'));
            this.currentIndex = index;
            this.open();
          });
        });
      });

      // Close handlers
      document.addEventListener('click', (e) => {
        if (e.target.closest('[data-lightbox-close]')) this.close();
        if (e.target.closest('[data-lightbox-prev]')) this.prev();
        if (e.target.closest('[data-lightbox-next]')) this.next();
      });

      document.addEventListener('keydown', (e) => {
        const lightbox = document.querySelector('.lightbox--open');
        if (!lightbox) return;
        if (e.key === 'Escape') this.close();
        if (e.key === 'ArrowLeft') this.prev();
        if (e.key === 'ArrowRight') this.next();
      });
    },

    open() {
      let lightbox = document.querySelector('[data-lightbox]');

      if (!lightbox) {
        lightbox = document.createElement('div');
        lightbox.className = 'lightbox';
        lightbox.setAttribute('data-lightbox', '');
        lightbox.innerHTML = `
          <button class="lightbox__close" data-lightbox-close aria-label="Close lightbox">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
          <button class="lightbox__nav lightbox__nav--prev" data-lightbox-prev aria-label="Previous image">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
          </button>
          <img class="lightbox__img" src="" alt="Screenshot">
          <button class="lightbox__nav lightbox__nav--next" data-lightbox-next aria-label="Next image">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
          </button>
        `;
        document.body.appendChild(lightbox);
      }

      const img = lightbox.querySelector('.lightbox__img');
      img.src = this.images[this.currentIndex];

      requestAnimationFrame(() => {
        lightbox.classList.add('lightbox--open');
      });

      document.body.classList.add('body-scroll-lock');
    },

    close() {
      const lightbox = document.querySelector('[data-lightbox]');
      if (lightbox) {
        lightbox.classList.remove('lightbox--open');
      }
      document.body.classList.remove('body-scroll-lock');
    },

    prev() {
      this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
      this.updateImage();
    },

    next() {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
      this.updateImage();
    },

    updateImage() {
      const lightbox = document.querySelector('[data-lightbox]');
      if (!lightbox) return;
      const img = lightbox.querySelector('.lightbox__img');
      img.src = this.images[this.currentIndex];
    }
  };


  /* --------------------------------------------------------------------------
     § 20. DROPDOWN CLOSE ON OUTSIDE CLICK
     -------------------------------------------------------------------------- */

  const DropdownManager = {
    init() {
      // Close dropdowns when clicking outside
      document.addEventListener('click', (e) => {
        if (!e.target.closest('.nav-dropdown')) {
          document.querySelectorAll('.nav-dropdown__panel').forEach((panel) => {
            // Only affects programmatically opened dropdowns, CSS :hover handles the rest
          });
        }
      });
    }
  };


  /* --------------------------------------------------------------------------
     § UTILITIES
     -------------------------------------------------------------------------- */

  function debounce(fn, delay) {
    let timer;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  }


  /* --------------------------------------------------------------------------
     § INITIALIZATION
     Boot all modules when DOM is ready.
     -------------------------------------------------------------------------- */

  function init() {
    ThemeManager.init();
    MobileMenu.init();
    SmoothScroll.init();
    CopyToClipboard.init();
    FAQAccordion.init();
    SearchOverlay.init();
    ScrollHeader.init();
    ScrollAnimations.init();
    TableFilters.init();
    BonusCarousel.init();
    QuizStepper.init();
    CountUp.init();
    TableOfContents.init();
    BackToTop.init();
    ToastManager.init();
    TabsComponent.init();
    ScoringBars.init();
    RatingWheel.init();
    Lightbox.init();
    DropdownManager.init();
  }

  // Boot on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();

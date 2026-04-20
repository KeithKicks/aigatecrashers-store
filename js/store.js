// AI Gatecrashers Store — Vanilla JS
// Premium digital product store: prompt packs, courses, business kits
(function () {
  'use strict';

  // ================================================================
  // CART STATE
  // ================================================================

  /** @type {Array<{id: string, name: string, price: number}>} */
  let cart = [];

  // ================================================================
  // INIT
  // ================================================================

  document.addEventListener('DOMContentLoaded', init);

  function init() {
    setupCart();
    setupFilters();
    setupFAQ();
    setupMobileMenu();
    setupNewsletter();
    setupOrderBumps();
    setupSmoothScroll();
    setupFadeAnimations();
    setupScrollTopButton();
  }

  // ================================================================
  // CART
  // ================================================================

  function setupCart() {
    // Wire up all add-to-cart buttons
    document.querySelectorAll('.js-add-to-cart').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var id    = btn.dataset.productId;
        var name  = btn.dataset.productName;
        var price = parseFloat(btn.dataset.productPrice);
        addToCart(id, name, price);
      });
    });

    // Cart toggle buttons (header icon, etc.)
    document.querySelectorAll('.js-toggle-cart').forEach(function (el) {
      el.addEventListener('click', toggleCart);
    });

    // Close cart when overlay is clicked
    var overlay = document.querySelector('.cart-overlay');
    if (overlay) {
      overlay.addEventListener('click', function () {
        closeCart();
      });
    }

    // Close cart with close button inside panel
    var closeBtn = document.querySelector('.cart-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        closeCart();
      });
    }

    // Keyboard: close cart on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        var panel = document.querySelector('.cart-panel');
        if (panel && panel.classList.contains('active')) {
          closeCart();
        }
      }
    });

    // Initialize UI (empty state on load)
    updateCartUI();
  }

  /**
   * Add a product to cart. If already present, open cart to show it.
   * @param {string} id
   * @param {string} name
   * @param {number} price
   */
  function addToCart(id, name, price) {
    var existing = cart.find(function (item) { return item.id === id; });

    if (existing) {
      // Digital products: no duplicates — just surface the cart
      openCart();
      return;
    }

    cart.push({ id: id, name: name, price: price });
    updateCartUI();
    openCart();
  }

  /**
   * Add to cart without opening the panel (used by order bumps).
   * @param {string} id
   * @param {string} name
   * @param {number} price
   */
  function addToCartSilent(id, name, price) {
    if (!cart.find(function (item) { return item.id === id; })) {
      cart.push({ id: id, name: name, price: price });
      updateCartUI();
    }
  }

  /**
   * Remove item from cart by index.
   * @param {number} index
   */
  function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartUI();
  }

  /**
   * Rebuild all cart-related DOM: count badges, item list, totals.
   */
  function updateCartUI() {
    // --- Count badges ---
    document.querySelectorAll('.cart-count').forEach(function (el) {
      el.textContent = cart.length;
      el.style.display = cart.length > 0 ? 'flex' : 'none';
    });

    // --- Item list ---
    var container = document.querySelector('.cart-items');
    if (!container) return;

    if (cart.length === 0) {
      container.innerHTML =
        '<div class="cart-empty"><p>Your cart is empty.</p></div>';
    } else {
      container.innerHTML = cart
        .map(function (item, i) {
          return (
            '<div class="cart-item">' +
              '<div class="cart-item-info">' +
                '<span class="cart-item-name">' + escapeHtml(item.name) + '</span>' +
                '<span class="cart-item-price">$' + item.price.toFixed(2) + '</span>' +
              '</div>' +
              '<button class="cart-item-remove" data-index="' + i + '" aria-label="Remove ' + escapeHtml(item.name) + '">&times;</button>' +
            '</div>'
          );
        })
        .join('');

      // Wire remove buttons (re-delegated after each render)
      container.querySelectorAll('.cart-item-remove').forEach(function (btn) {
        btn.addEventListener('click', function () {
          removeFromCart(parseInt(btn.dataset.index, 10));
        });
      });
    }

    // --- Cart total ---
    var total = cart.reduce(function (sum, item) { return sum + item.price; }, 0);
    document.querySelectorAll('.cart-total-amount').forEach(function (el) {
      el.textContent = '$' + total.toFixed(2);
    });
  }

  /** Open the cart panel. */
  function openCart() {
    var panel   = document.querySelector('.cart-panel');
    var overlay = document.querySelector('.cart-overlay');
    if (panel)   panel.classList.add('active');
    if (overlay) overlay.classList.add('active');
    document.body.classList.add('cart-open');
  }

  /** Close the cart panel. */
  function closeCart() {
    var panel   = document.querySelector('.cart-panel');
    var overlay = document.querySelector('.cart-overlay');
    if (panel)   panel.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    document.body.classList.remove('cart-open');
  }

  /** Toggle the cart open/closed. */
  function toggleCart() {
    var panel = document.querySelector('.cart-panel');
    if (panel && panel.classList.contains('active')) {
      closeCart();
    } else {
      openCart();
    }
  }

  // ================================================================
  // CATEGORY FILTERS
  // ================================================================

  function setupFilters() {
    var pills = document.querySelectorAll('.filter-pill');
    var cards = document.querySelectorAll('.product-card');

    if (!pills.length) return;

    pills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        var category = pill.dataset.category || 'all';

        // Update active state
        pills.forEach(function (p) { p.classList.remove('active'); });
        pill.classList.add('active');

        // Filter product cards with a smooth fade
        cards.forEach(function (card) {
          var match = category === 'all' || card.dataset.category === category;

          if (match) {
            card.style.display = '';
            // Small rAF delay so the display:'' takes effect before opacity
            requestAnimationFrame(function () {
              card.style.opacity = '1';
              card.style.transform = '';
            });
          } else {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.97)';
            setTimeout(function () {
              if (card.style.opacity === '0') {
                card.style.display = 'none';
              }
            }, 300);
          }
        });
      });
    });
  }

  // ================================================================
  // FAQ ACCORDION
  // ================================================================

  function setupFAQ() {
    document.querySelectorAll('.faq-section details').forEach(function (detail) {
      detail.addEventListener('toggle', function () {
        if (detail.open) {
          // Close sibling details in the same parent
          var siblings = detail.parentElement.querySelectorAll('details[open]');
          siblings.forEach(function (other) {
            if (other !== detail) other.open = false;
          });
        }
      });
    });
  }

  // ================================================================
  // MOBILE MENU
  // ================================================================

  function setupMobileMenu() {
    var toggle = document.querySelector('.mobile-menu-toggle');
    var nav    = document.querySelector('.nav-links');

    if (!toggle || !nav) return;

    toggle.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('active');
      toggle.classList.toggle('active', isOpen);
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close nav when a link inside is clicked
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('active');
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });

    // Close nav on outside click
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('active') &&
          !nav.contains(e.target) &&
          !toggle.contains(e.target)) {
        nav.classList.remove('active');
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ================================================================
  // NEWSLETTER
  // ================================================================

  function setupNewsletter() {
    document.querySelectorAll('.newsletter-form').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var input = form.querySelector('input[type="email"]');

        if (!input || !input.value.trim()) return;

        // Basic email format check
        var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRe.test(input.value.trim())) {
          input.style.borderColor = '#ef4444';
          input.focus();
          return;
        }

        // Success state
        var parent = form.parentElement;
        form.style.display = 'none';

        var msg = document.createElement('p');
        msg.className = 'success-message';
        msg.style.display = 'block';
        msg.textContent = "You\u2019re in! Check your email for your free prompts.";
        parent.appendChild(msg);
      });
    });
  }

  // ================================================================
  // ORDER BUMPS
  // ================================================================

  function setupOrderBumps() {
    document.querySelectorAll('.order-bump input[type="checkbox"]').forEach(function (cb) {
      cb.addEventListener('change', function () {
        var bump  = cb.closest('.order-bump');
        var id    = cb.dataset.bumpId;
        var name  = cb.dataset.bumpName;
        var price = parseFloat(cb.dataset.bumpPrice);

        bump.classList.toggle('checked', cb.checked);

        if (cb.checked) {
          addToCartSilent(id, name, price);
        } else {
          var idx = cart.findIndex(function (item) { return item.id === id; });
          if (idx > -1) removeFromCart(idx);
        }
      });
    });
  }

  // ================================================================
  // SMOOTH SCROLL
  // ================================================================

  function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var href = a.getAttribute('href');
        if (!href || href === '#') return;

        var target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  // ================================================================
  // FADE-IN ANIMATIONS (IntersectionObserver)
  // ================================================================

  function setupFadeAnimations() {
    if (!('IntersectionObserver' in window)) {
      // Fallback: show everything immediately
      document.querySelectorAll('.fade-in').forEach(function (el) {
        el.classList.add('visible');
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target); // fire once
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );

    document.querySelectorAll('.fade-in').forEach(function (el) {
      observer.observe(el);
    });
  }

  // ================================================================
  // SCROLL-TO-TOP BUTTON
  // ================================================================

  function setupScrollTopButton() {
    var btn = document.querySelector('.scroll-top');
    if (!btn) return;

    window.addEventListener('scroll', function () {
      btn.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ================================================================
  // UTILITIES
  // ================================================================

  /**
   * Safely escape HTML to prevent XSS when inserting user-facing data.
   * @param {string} str
   * @returns {string}
   */
  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ================================================================
  // PUBLIC API
  // ================================================================

  // Expose a minimal surface area for inline buttons / external scripts
  window.Store = {
    addToCart:      addToCart,
    removeFromCart: removeFromCart,
    toggleCart:     toggleCart,
    openCart:       openCart,
    closeCart:      closeCart,
    getCart:        function () { return cart.slice(); },
    getTotal:       function () {
      return cart.reduce(function (sum, item) { return sum + item.price; }, 0);
    }
  };

})();

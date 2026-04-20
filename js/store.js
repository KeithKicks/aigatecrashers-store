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
    setupSearch();
    setupSort();
    setupCheckout();
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
        var id           = btn.dataset.productId;
        var name         = btn.dataset.productName;
        var price        = parseFloat(btn.dataset.productPrice);
        var checkoutUrl  = btn.dataset.checkoutUrl || null;
        addToCart(id, name, price, checkoutUrl);
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
   * @param {string|null} [checkoutUrl] Stripe Payment Link URL for this product.
   */
  function addToCart(id, name, price, checkoutUrl) {
    var existing = cart.find(function (item) { return item.id === id; });

    if (existing) {
      // Digital products: no duplicates — just surface the cart
      openCart();
      return;
    }

    cart.push({ id: id, name: name, price: price, checkoutUrl: checkoutUrl || null });
    updateCartUI();
    openCart();
  }

  /**
   * Add to cart without opening the panel (used by order bumps).
   * @param {string} id
   * @param {string} name
   * @param {number} price
   * @param {string|null} [checkoutUrl]
   */
  function addToCartSilent(id, name, price, checkoutUrl) {
    if (!cart.find(function (item) { return item.id === id; })) {
      cart.push({ id: id, name: name, price: price, checkoutUrl: checkoutUrl || null });
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
  // CATEGORY FILTERS (legacy single-tag data-category + new multi-tag data-tags)
  // ================================================================

  function setupFilters() {
    var pills = document.querySelectorAll('.filter-pill');
    var cards = document.querySelectorAll('.product-card');

    if (!pills.length) return;

    pills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        var category = pill.dataset.filter || pill.dataset.category || 'all';

        // Update active state
        pills.forEach(function (p) { p.classList.remove('active'); });
        pill.classList.add('active');

        // Filter product cards with a smooth fade
        cards.forEach(function (card) {
          var match = cardMatchesCategory(card, category);
          applyCardVisibility(card, match);
        });
      });
    });
  }

  /**
   * Returns true if a product card matches the given category slug.
   * Supports multi-tag via `data-tags="tag1,tag2"` and legacy single `data-category`.
   */
  function cardMatchesCategory(card, category) {
    if (category === 'all') return true;
    var tagsAttr = (card.dataset.tags || card.dataset.category || '').toLowerCase();
    var tags = tagsAttr.split(',').map(function (t) { return t.trim(); });
    return tags.indexOf(category) !== -1;
  }

  function applyCardVisibility(card, visible) {
    if (visible) {
      card.classList.remove('hidden');
      card.style.display = '';
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
          card.classList.add('hidden');
        }
      }, 250);
    }
  }

  // ================================================================
  // SEARCH (client-side filter over product name + tags + description)
  // ================================================================

  function setupSearch() {
    var input = document.getElementById('store-search-input');
    if (!input) return;

    var cards = document.querySelectorAll('.product-card');
    var empty = document.getElementById('store-empty');

    function doSearch() {
      var q = (input.value || '').trim().toLowerCase();
      var anyVisible = false;

      cards.forEach(function (card) {
        if (q === '') {
          applyCardVisibility(card, true);
          anyVisible = true;
          return;
        }
        var title = (card.querySelector('.card-title') || {}).textContent || '';
        var desc  = (card.querySelector('.card-desc')  || {}).textContent || '';
        var tags  = card.dataset.tags || '';
        var hay = (title + ' ' + desc + ' ' + tags).toLowerCase();
        var match = hay.indexOf(q) !== -1;
        applyCardVisibility(card, match);
        if (match) anyVisible = true;
      });

      if (empty) empty.style.display = (q !== '' && !anyVisible) ? 'block' : 'none';

      // Hide entire category sections whose grids have no visible cards
      document.querySelectorAll('.category-section').forEach(function (section) {
        var visibleInSection = section.querySelectorAll('.product-card:not(.hidden)').length;
        section.style.display = (q !== '' && visibleInSection === 0) ? 'none' : '';
      });
    }

    // Debounced input handler
    var t = null;
    input.addEventListener('input', function () {
      clearTimeout(t);
      t = setTimeout(doSearch, 120);
    });

    // Clear on ESC
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        input.value = '';
        doSearch();
      }
    });
  }

  // ================================================================
  // SORT (most popular / price asc / price desc / newest)
  // ================================================================

  function setupSort() {
    var select = document.getElementById('store-sort-select');
    if (!select) return;

    select.addEventListener('change', function () {
      var mode = select.value;
      document.querySelectorAll('[data-category-grid]').forEach(function (grid) {
        var cards = Array.prototype.slice.call(grid.querySelectorAll('.product-card'));
        cards.sort(function (a, b) { return sortFn(a, b, mode); });
        cards.forEach(function (c) { grid.appendChild(c); });
      });
    });
  }

  function sortFn(a, b, mode) {
    switch (mode) {
      case 'price-asc':
        return num(a, 'price') - num(b, 'price');
      case 'price-desc':
        return num(b, 'price') - num(a, 'price');
      case 'newest':
        return (b.dataset.date || '').localeCompare(a.dataset.date || '');
      case 'popular':
      default:
        return num(b, 'popularity') - num(a, 'popularity');
    }
  }

  function num(el, key) {
    var v = parseFloat(el.dataset[key]);
    return isNaN(v) ? 0 : v;
  }

  // ================================================================
  // CHECKOUT (Stripe Payment Links)
  //
  // Each product's Add-to-Cart button carries data-checkout-url pointing
  // at its Stripe Payment Link. The cart's Checkout button routes to that
  // URL when the cart has exactly one item. Multi-item carts get a note
  // until a backend is wired up.
  // ================================================================

  function setupCheckout() {
    var btns = document.querySelectorAll('.cart-checkout, .js-checkout');
    if (!btns.length) return;

    btns.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        if (cart.length === 0) return;

        if (cart.length === 1) {
          var item = cart[0];
          if (item.checkoutUrl) {
            window.location.href = item.checkoutUrl;
            return;
          }
          // Fallback: no Stripe URL attached — send to support
          alert('This product is not yet wired up for instant checkout. Email Support@aigatecrashers.com and we will invoice you.');
          return;
        }

        // Multi-item: Stripe Payment Links are 1-item per link. For now, open each
        // in a new tab so the customer completes them in sequence. We'll replace
        // this with a single bundled checkout once a backend exists.
        var confirmed = confirm(
          'You have ' + cart.length + ' items in your cart.\n\n' +
          'Each will open in a new tab for separate checkout. ' +
          'Email us if you\u2019d prefer a single invoice.\n\nContinue?'
        );
        if (!confirmed) return;

        cart.forEach(function (item) {
          if (item.checkoutUrl) window.open(item.checkoutUrl, '_blank');
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
    // Prefer canonical `.mobile-nav` (dropdown dedicated to mobile).
    // Fall back to legacy `.nav-links` for older pages.
    var nav    = document.querySelector('.mobile-nav') || document.querySelector('.nav-links');

    if (!toggle || !nav) return;

    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
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
        var bump         = cb.closest('.order-bump');
        var id           = cb.dataset.bumpId;
        var name         = cb.dataset.bumpName;
        var price        = parseFloat(cb.dataset.bumpPrice);
        var checkoutUrl  = cb.dataset.checkoutUrl || null;

        bump.classList.toggle('checked', cb.checked);

        if (cb.checked) {
          addToCartSilent(id, name, price, checkoutUrl);
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

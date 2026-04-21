/* Site-wide nav behavior: scroll tint + mobile burger menu. Loaded on every page. */
(function(){
  const navWrap = document.getElementById('navWrap');
  if (!navWrap) return;

  // Scroll tint
  function onScroll(){
    navWrap.classList.toggle('scrolled', window.scrollY > 12);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile burger menu
  const burger = navWrap.querySelector('.nav-burger');
  const navLinks = navWrap.querySelector('.nav-links');
  if (!burger || !navLinks) return;

  // Inject "Get 50 free prompts" into mobile menu if not already present
  if (!navLinks.querySelector('.nav-menu-cta')){
    const ctaLink = document.createElement('a');
    ctaLink.href = '/#newsletter';
    ctaLink.className = 'nav-menu-cta';
    ctaLink.textContent = '✦ Get 50 free prompts';
    navLinks.appendChild(ctaLink);
  }

  burger.addEventListener('click', function(e){
    e.stopPropagation();
    const open = navLinks.classList.toggle('active');
    burger.classList.toggle('active', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  navLinks.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click', function(){
      navLinks.classList.remove('active');
      burger.classList.remove('active');
      burger.setAttribute('aria-expanded', 'false');
    });
  });

  document.addEventListener('click', function(e){
    if (navLinks.classList.contains('active') &&
        !navLinks.contains(e.target) && !burger.contains(e.target)){
      navLinks.classList.remove('active');
      burger.classList.remove('active');
      burger.setAttribute('aria-expanded', 'false');
    }
  });
})();

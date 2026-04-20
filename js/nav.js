/* Site-wide nav behavior: toggle .scrolled on scroll so the bar gets
   its tinted glass background + border. Loaded on every page. */
(function(){
  const navWrap = document.getElementById('navWrap');
  if (!navWrap) return;
  function onScroll(){
    navWrap.classList.toggle('scrolled', window.scrollY > 12);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

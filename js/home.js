/* =============================================================
   AI Gatecrashers — homepage interactions
   Extracted from the Claude Design mockup (April 2026).
   Attached only to index.html (live demo typing, nav scroll
   state, path-card mouse-tracking gradient).
   ============================================================= */

/* ---------- Nav scroll state ---------- */
(function(){
  const navWrap = document.getElementById('navWrap');
  if (!navWrap) return;
  function onScroll(){ navWrap.classList.toggle('scrolled', window.scrollY > 12); }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();
})();

/* ---------- Hover gradient tracking on path cards ---------- */
document.querySelectorAll('.path-card').forEach(function(el){
  el.addEventListener('mousemove', function(e){
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    el.style.setProperty('--my', (e.clientY - r.top) + 'px');
  });
});

/* ---------- Live demo typing animation ---------- */
(function(){
  const demoUserMsg = document.getElementById('demoUserMsg');
  const demoOutput  = document.getElementById('demoOutput');
  if (!demoUserMsg || !demoOutput) return;

  const DEMOS = {
    donor: {
      user: "I run a 3-person literacy non-profit. Draft a warm thank-you email to a donor who just gave $500.",
      out: `Subject: Thank you, Rosa — from our whole team

Dear Rosa,

Your $500 gift just became 40 tutoring hours for kids in the Eastside program. That's not a metaphor — that's the math. Forty kids, each getting an hour of one-on-one reading help this summer.

You didn't have to do this. You chose to. And on behalf of every kid who's going to sit down next to a volunteer because of you — thank you.

With warmth,
Maya`
    },
    grant: {
      user: "Write the opening paragraph of a grant application for a youth literacy program serving 200 kids.",
      out: `Three out of four kids at Lincoln Elementary read below grade level. We've been inside that school every Tuesday for six years, and we know two things for certain: the gap is closable, and the kids already know they're behind. This proposal asks for $42,000 to expand our one-on-one tutoring model to 200 students over the 2026–27 year...`
    },
    sop: {
      user: "Create a simple SOP for how our front-desk team should respond to after-hours email inquiries.",
      out: `SOP: After-hours email response
Owner: Front desk  |  Review: Monthly

1. Open the inbox by 8:45 AM.
2. Sort emails into: "Urgent", "Standard", "Spam".
3. For Urgent: reply within 15 min using the "After-hours apology" template (linked below).
4. For Standard: reply within 2 hours with next available appointment.
5. Flag anything mentioning billing, legal, or medical for owner review.`
    },
    social: {
      user: "Write a friendly Instagram post announcing our Saturday volunteer day to our existing followers.",
      out: `This Saturday we're painting the reading room at Lincoln Elementary 💛

Coffee at 9. Paintbrushes at 9:15. Done by noon — we promise.

Bring: old clothes, a friend, zero experience needed. We've got the rest.

Comment "IN" below and we'll send the address. 🎨`
    }
  };

  let typingTimer = null;

  function typeDemo(key){
    const d = DEMOS[key];
    if (!d) return;
    demoUserMsg.textContent = d.user;
    demoOutput.innerHTML = '';
    const full = d.out;
    let i = 0;
    clearTimeout(typingTimer);
    (function tick(){
      i += Math.max(1, Math.round(Math.random() * 3));
      if (i > full.length) i = full.length;
      demoOutput.innerHTML = full.slice(0, i).replace(/\n/g, '<br/>') + '<span class="cursor"></span>';
      if (i < full.length) {
        typingTimer = setTimeout(tick, 14 + Math.random() * 28);
      }
    })();
  }

  document.querySelectorAll('[data-demo]').forEach(function(btn){
    btn.addEventListener('click', function(){
      document.querySelectorAll('[data-demo]').forEach(function(b){
        b.classList.toggle('active', b === btn);
      });
      typeDemo(btn.dataset.demo);
    });
  });

  typeDemo('donor');
})();

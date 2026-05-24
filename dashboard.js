/* IPL Crunch '26 — Dashboard Interactivity */
document.addEventListener('DOMContentLoaded', () => {

  // ===== TAB NAVIGATION =====
  const tabs = document.querySelectorAll('.nav-tab');
  const sections = document.querySelectorAll('.section');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      sections.forEach(s => {
        s.classList.remove('active');
        if (s.id === `sec-${target}`) {
          s.classList.add('active');
          // Trigger chart reveal animations
          s.querySelectorAll('.chart-card, .insight-card').forEach((card, i) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
              card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
              card.style.opacity = '1';
              card.style.transform = 'translateY(0)';
            }, i * 100);
          });
        }
      });
    });
  });

  // ===== ANIMATED COUNTERS =====
  const counters = document.querySelectorAll('.stat-value[data-target]');
  let countersAnimated = false;

  function animateCounters() {
    if (countersAnimated) return;
    countersAnimated = true;
    counters.forEach(counter => {
      const target = parseInt(counter.dataset.target);
      const duration = 2000;
      const start = performance.now();

      function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(eased * target);
        counter.textContent = current.toLocaleString();
        if (progress < 1) requestAnimationFrame(update);
      }
      requestAnimationFrame(update);
    });
  }

  // Trigger counters when stats row is visible
  const statsRow = document.querySelector('.stats-row');
  if (statsRow) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounters();
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    observer.observe(statsRow);
  }

  // ===== SCROLL REVEAL FOR CARDS =====
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  // Initial reveal setup for first visible section
  document.querySelectorAll('.section.active .chart-card, .section.active .insight-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    revealObserver.observe(card);
  });

  // ===== IMAGE LAZY LOAD FALLBACK =====
  document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', () => {
      img.style.display = 'none';
      const placeholder = document.createElement('div');
      placeholder.style.cssText = 'padding:3rem;text-align:center;color:#64748b;background:#1a2332;border-radius:8px;border:1px dashed #2a3a4a;';
      placeholder.textContent = '📊 Chart not yet generated — run analyze_ipl.py first';
      img.parentNode.insertBefore(placeholder, img.nextSibling);
    });
  });

});

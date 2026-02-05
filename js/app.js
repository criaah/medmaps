// MedMaps - App Logic v2

document.addEventListener('DOMContentLoaded', function() {
  initializeHamburgerMenu();
  initializeAccordions();
  initializeSearch();
  initializeThemeToggle();
  initializeScrollReveal();
  initializeToggleLists();
  initializeModal();
});

// HAMBURGER MENU
function initializeHamburgerMenu() {
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('nav ul');
  if (!hamburger || !navMenu) return;
  hamburger.addEventListener('click', function() {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
  });
  navMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      navMenu.classList.remove('active');
    });
  });
  document.addEventListener('click', function(e) {
    if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
      hamburger.classList.remove('active');
      navMenu.classList.remove('active');
    }
  });
}

// ACCORDION FUNCTIONALITY
function initializeAccordions() {
  const headers = document.querySelectorAll('.accordion-header');
  headers.forEach(header => {
    header.addEventListener('click', function() {
      this.classList.toggle('active');
      this.nextElementSibling.classList.toggle('active');
    });
  });
}

// SEARCH FUNCTIONALITY
function initializeSearch() {
  const searchInput = document.getElementById('searchInput');
  const searchBtn = document.getElementById('searchBtn');
  if (!searchInput) return;
  function performSearch() {
    const query = searchInput.value.toLowerCase().trim();
    const cards = document.querySelectorAll('[data-searchable]');
    const accordions = document.querySelectorAll('.accordion');
    let found = 0;
    cards.forEach(card => {
      const text = card.getAttribute('data-searchable').toLowerCase() + ' ' + card.textContent.toLowerCase();
      if (text.includes(query) || query === '') {
        card.style.display = '';
        found++;
      } else {
        card.style.display = 'none';
      }
    });
    accordions.forEach(accordion => {
      const specialty = accordion.getAttribute('data-searchable') || '';
      const mapItems = accordion.querySelectorAll('.map-item');
      let hasVisibleMaps = false;
      mapItems.forEach(map => {
        const mapText = (map.getAttribute('data-searchable') || map.textContent).toLowerCase();
        if (mapText.includes(query) || specialty.toLowerCase().includes(query) || query === '') {
          map.style.display = '';
          hasVisibleMaps = true;
        } else {
          map.style.display = 'none';
        }
      });
      if (hasVisibleMaps || specialty.toLowerCase().includes(query) || query === '') {
        accordion.style.display = '';
        if (query !== '' && hasVisibleMaps) {
          const header = accordion.querySelector('.accordion-header');
          const content = accordion.querySelector('.accordion-content');
          if (header && content) {
            header.classList.add('active');
            content.classList.add('active');
          }
        }
      } else {
        accordion.style.display = 'none';
      }
    });
    const noResults = document.getElementById('noResults');
    if (noResults) {
      const visibleItems = document.querySelectorAll('.accordion:not([style*="display: none"]), .card:not([style*="display: none"])');
      noResults.style.display = visibleItems.length === 0 && query !== '' ? 'block' : 'none';
    }
  }
  searchInput.addEventListener('keyup', performSearch);
  searchInput.addEventListener('search', performSearch);
  if (searchBtn) {
    searchBtn.addEventListener('click', performSearch);
  }
}

// THEME TOGGLE (DARK MODE)
function initializeThemeToggle() {
  const themeToggle = document.getElementById('themeToggle');
  if (!themeToggle) return;
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.body.classList.toggle('dark-mode', savedTheme === 'dark');
  updateThemeIcon();
  themeToggle.addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    updateThemeIcon();
  });
}

function updateThemeIcon() {
  const themeToggle = document.getElementById('themeToggle');
  if (!themeToggle) return;
  const isDarkMode = document.body.classList.contains('dark-mode');
  themeToggle.textContent = isDarkMode ? '☀️' : '🌙';
}

// SCROLL REVEAL ANIMATION
function initializeScrollReveal() {
  const revealElements = document.querySelectorAll('[data-reveal]');
  if (!window.IntersectionObserver) return;
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  revealElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s, transform 0.6s';
    observer.observe(el);
  });
}

// TOGGLE LIST FUNCTIONALITY
function initializeToggleLists() {
  document.addEventListener('click', function(e) {
    const header = e.target.closest('.toggle-header');
    if (!header) return;
    header.classList.toggle('expanded');
    const content = header.nextElementSibling;
    if (content && content.classList.contains('toggle-content')) {
      content.classList.toggle('visible');
    }
    const children = header.parentElement.querySelector('.toggle-children');
    if (children) {
      children.classList.toggle('visible');
    }
  });
}

// MODAL FUNCTIONALITY
function initializeModal() {
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
      closeModal();
    }
  });
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-close')) {
      closeModal();
    }
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      closeModal();
    }
  });
}

function openModal(title, content) {
  let modal = document.getElementById('mapModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'mapModal';
    modal.className = 'modal-overlay';
    modal.innerHTML = '<div class="modal"><div class="modal-header"><h2 id="modalTitle"></h2><button class="modal-close">&times;</button></div><div class="modal-body" id="modalBody"></div><div class="modal-footer"><button class="btn btn-secondary btn-small" onclick="closeModal()">Cerrar</button></div></div>';
    document.body.appendChild(modal);
  }
  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalBody').innerHTML = content;
  modal.classList.add('visible');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  const modal = document.getElementById('mapModal');
  if (modal) {
    modal.classList.remove('visible');
    document.body.style.overflow = '';
  }
}

// FILTER MAPS BY STATUS
function filterMaps(status) {
  const maps = document.querySelectorAll('[data-map]');
  maps.forEach(map => {
    if (status === 'all' || map.getAttribute('data-map') === status) {
      map.style.display = '';
    } else {
      map.style.display = 'none';
    }
  });
}

// PAYMENT INTEGRATION (Placeholder for Lemon Squeezy)
function initiatePremiumPayment(planId) {
  console.log('Premium payment initiated for plan:', planId);
  alert('¡Gracias por tu interés! La integración de pagos estará disponible pronto.');
}

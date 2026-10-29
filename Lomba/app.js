// ===== SIBSKU — SHARED APP.JS =====
// Navigation router, mock data, toast, shared utilities

// ===== PAGE ROUTING =====
// Maps data-path values → actual HTML files
const ROUTES = {
  'overview':               'dashboard.html',
  'facetime':               'videochat.html',
  'sign-translation':       'videochat.html',
  'account':                'profile.html',
  'settings':               'profile.html',
  'privacy':                'index.html#privacy',
  'accessibility-statement':'index.html#accessibility',
  'community-guidelines':   'index.html#',
};

// Wire every [data-path] anchor/button to the correct file
(function wireNavigation() {
  document.querySelectorAll('[data-path]').forEach(el => {
    const path  = el.getAttribute('data-path');
    const route = ROUTES[path];
    if (!route) return;

    if (el.tagName === 'A') {
      el.setAttribute('href', route);
    } else {
      // button or div — navigate on click
      el.style.cursor = 'pointer';
      el.addEventListener('click', () => { window.location.href = route; });
    }
  });
})();

// Highlight active nav link based on current page filename
(function highlightNav() {
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('[data-path]').forEach(el => {
    const path  = el.getAttribute('data-path');
    const route = ROUTES[path] || '';
    const isActive = route === page || (page === '' && route === 'dashboard.html');
    if (isActive) {
      el.classList.add('text-on-surface', 'font-medium', 'border-b', 'border-on-surface');
      el.classList.remove('text-on-surface-variant', 'text-secondary');
      el.setAttribute('aria-current', 'page');
    }
  });
})();

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'info', duration = 3500) {
  // Tailwind-based pages use a toast container we inject; styles.css pages have #toastContainer
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.cssText = [
      'position:fixed', 'bottom:1.25rem', 'right:1.25rem', 'z-index:9999',
      'display:flex', 'flex-direction:column', 'gap:0.5rem',
      'pointer-events:none',
    ].join(';');
    document.body.appendChild(container);
  }

  const colorMap = {
    success: '#00e5a0',
    error:   '#ff4d6d',
    warning: '#f7c948',
    info:    '#00d4ff',
  };
  const accent = colorMap[type] || colorMap.info;

  const toast = document.createElement('div');
  toast.style.cssText = [
    'background:#111525',
    'border:1px solid rgba(255,255,255,0.07)',
    `border-left:3px solid ${accent}`,
    'border-radius:8px',
    'padding:0.65rem 1rem',
    'min-width:260px',
    'max-width:340px',
    'display:flex',
    'align-items:center',
    'gap:0.625rem',
    'font-size:0.8125rem',
    'color:#e8eeff',
    'font-family:inherit',
    'box-shadow:0 4px 20px rgba(0,0,0,0.7)',
    'pointer-events:all',
    'opacity:0',
    'transform:translateY(8px)',
    'transition:opacity 0.25s ease,transform 0.25s ease',
  ].join(';');

  toast.innerHTML = `
    <span style="flex:1;line-height:1.5;">${message}</span>
    <button onclick="this.parentElement.remove()" style="background:none;border:none;color:rgba(255,255,255,0.3);cursor:pointer;font-size:1rem;line-height:1;padding:0;flex-shrink:0;">✕</button>
  `;
  container.appendChild(toast);

  // Animate in
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateY(0)';
    });
  });

  // Auto-remove
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(12px)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// ===== MOCK DATA =====
const MOCK_USERS = [
  { id: 1,  name: 'Aiko Tanaka',   country: 'Japan',   avatar: 'A', accessibility: true  },
  { id: 2,  name: 'Marco Silva',   country: 'Brazil',  avatar: 'M', accessibility: false },
  { id: 3,  name: 'Sophie Martin', country: 'France',  avatar: 'S', accessibility: false },
  { id: 4,  name: 'Liam Carter',   country: 'USA',     avatar: 'L', accessibility: false },
  { id: 5,  name: 'Chen Wei',      country: 'China',   avatar: 'C', accessibility: true  },
  { id: 6,  name: 'Priya Sharma',  country: 'India',   avatar: 'P', accessibility: true  },
  { id: 7,  name: 'Lars Hansen',   country: 'Denmark', avatar: 'L', accessibility: false },
  { id: 8,  name: 'Yuki Yoshida',  country: 'Japan',   avatar: 'Y', accessibility: true  },
  { id: 9,  name: 'Ana González',  country: 'Spain',   avatar: 'A', accessibility: false },
  { id: 10, name: 'Oliver Brown',  country: 'UK',      avatar: 'O', accessibility: false },
];

const MOCK_SIGNS = [
  'Hello! Nice to meet you',
  'Where are you from?',
  'I love your country',
  'How old are you?',
  'What do you do for work?',
  'This AI translation is amazing',
  'I am learning sign language',
  'Thank you for chatting with me',
  'You seem very kind',
  'See you again soon',
  'I love to travel',
  'What is your hobby?',
  'The weather is nice today',
  'I enjoy music',
  'Nice to connect with you!',
];

function getRandomPartner() {
  return MOCK_USERS[Math.floor(Math.random() * MOCK_USERS.length)];
}
function getRandomSign() {
  return MOCK_SIGNS[Math.floor(Math.random() * MOCK_SIGNS.length)];
}

// ===== LOCAL STORAGE HELPERS =====
const STORAGE_KEY = 'sibsku_user';
const DEFAULT_USER = {
  firstName: 'Rayhan', lastName: 'Pratama',
  email: 'rayhan@example.com', country: 'Indonesia',
  accessibility: true, avatar: 'R',
};

function saveUser(data) { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch(_) {} }
function getUser()      { try { const r = localStorage.getItem(STORAGE_KEY); return r ? JSON.parse(r) : null; } catch(_) { return null; } }
function clearUser()    { try { localStorage.removeItem(STORAGE_KEY); } catch(_) {} }

if (!getUser()) saveUser(DEFAULT_USER);

// ===== ESC CLOSES MODALS (styles.css pages) =====
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.show').forEach(m => m.classList.remove('show'));
  }
});

// Click outside modal to close
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', e => {
    if (e.target === overlay) overlay.classList.remove('show');
  });
});

// ===== SCROLL ANIMATIONS (styles.css pages) =====
const ioOpts = { threshold: 0.1, rootMargin: '0px 0px -30px 0px' };
const io = new IntersectionObserver((entries, obs) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'translateY(0)';
      obs.unobserve(e.target);
    }
  });
}, ioOpts);

document.querySelectorAll('.card, .glass-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
  io.observe(el);
});

// ===== FORMAT HELPERS =====
function formatTime(s) {
  return String(Math.floor(s/60)).padStart(2,'0') + ':' + String(s%60).padStart(2,'0');
}

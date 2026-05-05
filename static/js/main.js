document.getElementById('id_make')?.addEventListener('change', function () {
  const make = this.value;
  fetch(`/cars/ajax/models/?make=${make}`)
    .then((r) => r.json())
    .then((data) => {
      const modelSelect = document.getElementById('id_model_name');
      if (!modelSelect) return;
      modelSelect.innerHTML = '<option value="">Модель: любая</option>';
      data.models.forEach((m) => {
        modelSelect.innerHTML += `<option value="${m}">${m}</option>`;
      });
    });
});

const qsMake = document.getElementById('qs-make');
const qsModel = document.getElementById('qs-model');
if (qsMake && qsModel && typeof MODELS_BY_MAKE !== 'undefined') {
  qsMake.addEventListener('change', function () {
    const make = this.value;
    qsModel.innerHTML = '<option value="">Модель: любая</option>';
    if (make && MODELS_BY_MAKE[make]) {
      MODELS_BY_MAKE[make].forEach(function (m) {
        qsModel.innerHTML += `<option value="${m}">${m}</option>`;
      });
    }
  });
}

document.addEventListener('click', function (e) {
  const btn = e.target.closest('.btn-favorite');
  if (!btn) return;
  e.preventDefault();
  e.stopPropagation();
  const id = btn.dataset.id;
  if (!id) return;
  fetch('/cars/ajax/favorite/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `listing_id=${id}`,
  })
    .then((r) => r.json())
    .then((data) => {
      if (data.status === 'added') {
        btn.classList.add('active');
        btn.innerHTML = '♥';
      } else {
        btn.classList.remove('active');
        btn.innerHTML = '♡';
      }
    })
    .catch((err) => console.error('Favorite error:', err));
});

document.querySelectorAll('.thumb-img').forEach((thumb) => {
  thumb.addEventListener('click', function () {
    const main = document.getElementById('main-photo');
    if (main) main.src = this.dataset.full;
  });
});

document.getElementById('toggle-advanced')?.addEventListener('click', function () {
  document.getElementById('advanced-filters')?.classList.toggle('d-none');
});

// ============================================================
// МНОЖЕСТВЕННАЯ ЗАГРУЗКА ФОТО — накапливаем до 10 файлов
// ============================================================
(function() {
  const MAX_PHOTOS = 10;
  let collectedFiles = [];

  const dropZone = document.getElementById('photo-drop-zone');
  const fileInput = document.getElementById('photo-file-input');
  const preview = document.getElementById('photo-preview');
  const countText = document.getElementById('photo-count-text');
  const hiddenInputs = document.getElementById('photo-hidden-inputs');

  if (!dropZone || !fileInput) return;

  dropZone.addEventListener('click', function(e) {
    if (e.target !== fileInput) {
      fileInput.value = '';
      fileInput.click();
    }
  });

  fileInput.addEventListener('change', function() {
    const newFiles = Array.from(this.files);
    addFiles(newFiles);
  });

  dropZone.addEventListener('dragover', function(e) {
    e.preventDefault();
    dropZone.style.borderColor = 'var(--primary)';
  });
  dropZone.addEventListener('dragleave', function() {
    dropZone.style.borderColor = '#333';
  });
  dropZone.addEventListener('drop', function(e) {
    e.preventDefault();
    dropZone.style.borderColor = '#333';
    addFiles(Array.from(e.dataTransfer.files));
  });

  function addFiles(newFiles) {
    const images = newFiles.filter((f) => f.type.startsWith('image/'));
    const remaining = MAX_PHOTOS - collectedFiles.length;
    const toAdd = images.slice(0, remaining);

    if (toAdd.length === 0) {
      if (collectedFiles.length >= MAX_PHOTOS) {
        alert('Максимум 10 фотографий');
      }
      return;
    }

    collectedFiles = collectedFiles.concat(toAdd);
    renderPreviews();
    updateHiddenInputs();
    updateCount();
  }

  function renderPreviews() {
    preview.innerHTML = '';
    collectedFiles.forEach(function(file, idx) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const wrap = document.createElement('div');
        wrap.className = 'preview-item position-relative';
        wrap.innerHTML = `
          <img src="${e.target.result}" class="preview-thumb ${idx === 0 ? 'preview-main' : ''}" alt="фото ${idx + 1}">
          ${idx === 0 ? '<span class="preview-main-label">Главное</span>' : ''}
          <button type="button" class="preview-remove" data-idx="${idx}" title="Удалить">✕</button>
        `;
        preview.appendChild(wrap);

        wrap.querySelector('.preview-remove').addEventListener('click', function() {
          collectedFiles.splice(parseInt(this.dataset.idx, 10), 1);
          renderPreviews();
          updateHiddenInputs();
          updateCount();
        });
      };
      reader.readAsDataURL(file);
    });
  }

  function updateHiddenInputs() {
    hiddenInputs.innerHTML = '';

    if (collectedFiles.length === 0) return;

    const dt = new DataTransfer();
    collectedFiles.forEach(function(f) { dt.items.add(f); });

    const inp = document.createElement('input');
    inp.type = 'file';
    inp.name = 'photos';
    inp.multiple = true;
    inp.className = 'd-none';
    try {
      inp.files = dt.files;
    } catch(e) {
      // fallback для старых браузеров
    }

    hiddenInputs.innerHTML = '';
    collectedFiles.forEach(function(file) {
      const singleDt = new DataTransfer();
      singleDt.items.add(file);
      const singleInp = document.createElement('input');
      singleInp.type = 'file';
      singleInp.name = 'photos';
      singleInp.className = 'd-none';
      try {
        singleInp.files = singleDt.files;
      } catch(e) {}
      hiddenInputs.appendChild(singleInp);
    });
  }

  function updateCount() {
    if (countText) {
      const n = collectedFiles.length;
      countText.textContent = n > 0 ? `Выбрано фото: ${n} / ${MAX_PHOTOS}` : '';
    }
  }
})();

function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (const c of cookies) {
    const [k, v] = c.trim().split('=');
    if (k === name) return decodeURIComponent(v);
  }
  return null;
}

function toggleDetailFavorite(btn) {
  const id = btn.dataset.id;
  fetch('/cars/ajax/favorite/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `listing_id=${id}`,
  })
    .then((r) => r.json())
    .then((data) => {
      if (data.status === 'added') {
        btn.className = 'btn btn-danger detail-btn';
        btn.innerHTML = '♥ В избранном';
      } else {
        btn.className = 'btn btn-outline-light detail-btn';
        btn.innerHTML = '♡ В избранное';
      }
    })
    .catch((err) => console.error('Favorite error:', err));
}

// ============================================================
// АНИМАЦИИ ПРИ СКРОЛЛЕ (Intersection Observer)
// ============================================================
(function() {
  const sections = document.querySelectorAll('[data-animate]');
  const sectionObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        sectionObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  sections.forEach(function(el) { sectionObserver.observe(el); });

  const cards = document.querySelectorAll('.cars-grid .car-card');
  const cardObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        setTimeout(function() {
          entry.target.classList.add('card-visible');
        }, (entry.target.dataset.cardIdx || 0) * 80);
        cardObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  cards.forEach(function(card, i) {
    card.dataset.cardIdx = i;
    cardObserver.observe(card);
  });

  const whyItems = document.querySelectorAll('.why-item');
  const whyObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        whyObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });
  whyItems.forEach(function(el) { whyObserver.observe(el); });

  const counters = document.querySelectorAll('[data-count]');
  const counterObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.closest('.counter-item')?.classList.add('in-view');
        animateCount(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  counters.forEach(function(el) { counterObserver.observe(el); });

  function animateCount(el) {
    const target = parseInt(el.dataset.count, 10);
    const duration = 1800;
    const start = performance.now();
    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(eased * target).toLocaleString('ru');
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  const heroBg = document.querySelector('.hero-bg');
  if (heroBg) {
    window.addEventListener('scroll', function() {
      const scrolled = window.pageYOffset;
      if (scrolled < window.innerHeight) {
        heroBg.style.transform = `scale(1.05) translateY(${scrolled * 0.25}px)`;
      }
    }, { passive: true });
  }
})();

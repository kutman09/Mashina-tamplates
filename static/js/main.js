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

document.getElementById('photo-upload')?.addEventListener('change', function () {
  const preview = document.getElementById('photo-preview');
  if (!preview) return;
  preview.innerHTML = '';
  [...this.files].forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.innerHTML += `<img src="${e.target.result}" class="preview-thumb">`;
    };
    reader.readAsDataURL(file);
  });
});

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

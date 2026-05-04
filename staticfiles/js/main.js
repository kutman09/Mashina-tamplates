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

document.querySelectorAll('.btn-favorite').forEach((btn) => {
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    const id = this.dataset.id;
    fetch('/cars/ajax/favorite/', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `listing_id=${id}`,
    })
      .then((r) => r.json())
      .then((data) => {
        this.classList.toggle('active', data.status === 'added');
        this.textContent = data.status === 'added' ? '♥' : '♡';
      });
  });
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
      preview.innerHTML += `<img src="${e.target.result}" style="width:80px;height:60px;object-fit:cover">`;
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

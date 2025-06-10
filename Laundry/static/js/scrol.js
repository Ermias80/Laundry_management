
  window.addEventListener('scroll', function () {
    const backTop = document.getElementById('back-top');
    if (window.scrollY > 100) {
      backTop.style.display = 'block';
    } else {
      backTop.style.display = 'none';
    }
  });

  document.getElementById('back-top').addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
 document.querySelector('.logo a').addEventListener('click', e => e.preventDefault());
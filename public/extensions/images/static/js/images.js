window.CustomUtils.toggleLightbox = (el) => {
  document.querySelector(".lightbox-image").src = el.querySelector("img").src;
  document.querySelector(".lightbox-caption").innerHTML = el.querySelector(".caption").innerHTML;
  $("#lightbox").modal("show");
};

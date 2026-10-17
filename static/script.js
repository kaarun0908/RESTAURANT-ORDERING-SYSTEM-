document.addEventListener("DOMContentLoaded", () => {
  // Smooth horizontal carousels.
  document.querySelectorAll("[data-scroll]").forEach(button => {
    button.addEventListener("click", () => {
      const row = document.getElementById(button.dataset.scroll);
      if (row) row.scrollBy({ left: Number(button.dataset.dir) * row.clientWidth * 0.8, behavior: "smooth" });
    });
  });

  // Location selector popup.
  const locationButton = document.getElementById("locationButton");
  const locationPopup = document.getElementById("locationPopup");
  const locationText = document.getElementById("locationText");
  const locationInput = document.getElementById("locationInput");
  locationButton?.addEventListener("click", () => locationPopup.classList.toggle("open"));
  document.getElementById("saveLocation")?.addEventListener("click", () => {
    const value = locationInput.value.trim();
    if (value) {
      locationText.textContent = value;
      locationPopup.classList.remove("open");
    }
  });
  document.addEventListener("click", event => {
    if (locationPopup && !locationPopup.contains(event.target) && !locationButton.contains(event.target)) {
      locationPopup.classList.remove("open");
    }
  });

  const searchInput = document.getElementById("searchInput");
  const cards = [...document.querySelectorAll(".food-card")];
  const sortSelect = document.getElementById("sortSelect");
  const emptyState = document.getElementById("emptyState");
  let activeFilter = "all";

  function refreshMenu() {
    const query = (searchInput?.value || "").toLowerCase().trim();
    const sorted = [...cards].sort((a, b) => {
      if (sortSelect?.value === "rating") return Number(b.dataset.rating) - Number(a.dataset.rating);
      if (sortSelect?.value === "low") return Number(a.dataset.price) - Number(b.dataset.price);
      if (sortSelect?.value === "high") return Number(b.dataset.price) - Number(a.dataset.price);
      return cards.indexOf(a) - cards.indexOf(b);
    });
    let visible = 0;
    sorted.forEach(card => {
      const matchesText = (card.dataset.name + " " + card.dataset.category).includes(query);
      const matchesFilter = activeFilter === "all" ||
        (activeFilter === "veg" && card.dataset.veg === "true") ||
        (activeFilter === "fast" && Number(card.dataset.rating) >= 4.5);
      card.hidden = !(matchesText && matchesFilter);
      if (!card.hidden) visible++;
      document.getElementById("foodGrid").appendChild(card);
    });
    if (emptyState) emptyState.hidden = visible !== 0;
  }
  searchInput?.addEventListener("input", refreshMenu);
  sortSelect?.addEventListener("change", refreshMenu);
  document.querySelectorAll("[data-filter]").forEach(button => {
    button.addEventListener("click", () => {
      activeFilter = button.dataset.filter;
      document.querySelectorAll("[data-filter]").forEach(chip => chip.classList.toggle("active", chip === button));
      refreshMenu();
    });
  });
  document.querySelectorAll(".category").forEach(button => {
    button.addEventListener("click", () => {
      if (searchInput) searchInput.value = button.dataset.category;
      document.getElementById("menu")?.scrollIntoView({ behavior: "smooth" });
      refreshMenu();
    });
  });
});

(function () {
  const scenes = window.GALLERY || [];
  const grid = document.getElementById("grid");
  const filters = document.getElementById("filters");
  const PAGE = 24;
  let source = "All";
  let shown = PAGE;

  const counts = scenes.reduce((acc, s) => ((acc[s.src] = (acc[s.src] || 0) + 1), acc), {});
  const sources = ["All", ...Object.keys(counts)];

  function el(tag, cls, text) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  function card(s) {
    const c = el("div", "scene");
    const pics = el("div", "pics");
    const sim = el("img", "sim");
    sim.src = `static/gallery/${s.img}_sim.jpg`;
    sim.alt = `Simulation scene ${s.id}`;
    sim.loading = "lazy";
    const real = el("img", "real");
    real.src = `static/gallery/${s.img}_real.jpg`;
    real.alt = `Source video frame ${s.id}`;
    real.loading = "lazy";
    pics.append(sim, real, el("span", "tag s", "SIM"), el("span", "tag r", "SOURCE VIDEO"));
    pics.addEventListener("click", () => pics.classList.toggle("show"));
    const meta = el("div", "meta");
    const id = el("div", "id");
    id.append(el("span", "", s.id), el("em", "", s.src));
    meta.append(id, el("p", "task", s.task));
    c.append(pics, meta);
    return c;
  }

  function render() {
    const list = scenes.filter((s) => source === "All" || s.src === source);
    grid.replaceChildren(...list.slice(0, shown).map(card));
    const old = document.getElementById("more");
    if (old) old.remove();
    if (list.length > shown) {
      const wrap = el("div", "more");
      wrap.id = "more";
      const b = el("button", "btn", `Show all ${list.length} scenes`);
      b.addEventListener("click", () => {
        shown = Infinity;
        render();
      });
      wrap.append(b);
      grid.after(wrap);
    }
  }

  sources.forEach((name) => {
    const b = el("button", name === source ? "on" : "", name);
    b.append(el("span", "", name === "All" ? scenes.length : counts[name]));
    b.addEventListener("click", () => {
      source = name;
      shown = PAGE;
      filters.querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
      render();
    });
    filters.append(b);
  });

  render();
})();

"use strict";

/* CaseFinder — static, dependency-free compatibility lookup.
   Security: rendering uses only textContent/createElement — never raw
   HTML sinks — so no value from the dataset can be interpreted as markup. */

const brandSel = document.getElementById("brand");
const modelSel = document.getElementById("model");
const form = document.getElementById("finder");
const result = document.getElementById("result");

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) {
    node.className = className;
  }
  if (text !== undefined && text !== null) {
    node.textContent = String(text);
  }
  return node;
}

function clear(node) {
  while (node.firstChild) {
    node.removeChild(node.firstChild);
  }
}

function uniqueSorted(values) {
  return Array.from(new Set(values)).sort((a, b) => a.localeCompare(b));
}

function fillBrands(phones) {
  clear(brandSel);
  brandSel.appendChild(el("option", null, "Select a brand..."));
  uniqueSorted(phones.map((p) => p.brand)).forEach((brand) => {
    const opt = el("option", null, brand);
    opt.value = brand;
    brandSel.appendChild(opt);
  });
}

function fillModels(phones, brand) {
  clear(modelSel);
  modelSel.disabled = !brand;
  if (!brand) {
    return;
  }
  const rows = phones
    .filter((p) => p.brand === brand)
    .sort((a, b) => a.model.localeCompare(b.model));
  modelSel.appendChild(el("option", null, "Select a model..."));
  rows.forEach((p) => {
    const opt = el("option", null, p.model);
    opt.value = p.id;
    modelSel.appendChild(opt);
  });
}

function showError(message) {
  result.hidden = false;
  clear(result);
  result.appendChild(el("p", null, message));
}

function render(phone) {
  clear(result);
  const d = phone.dimensionsMm;

  result.appendChild(el("h2", null, phone.brand + " " + phone.model));

  const dl = el("dl");
  const addRow = (key, value) => {
    dl.appendChild(el("dt", null, key));
    dl.appendChild(el("dd", null, value));
  };

  addRow("Released", phone.releaseYear);

  if (d && d.h) {
    addRow("Dimensions", d.h + " x " + d.w + " x " + d.t + " mm");
  }

  addRow("MagSafe", phone.magsafe ? "Yes" : "No");

  const sp = phone.screenProtector || {};
  if (sp.type) {
    addRow(
      "Screen protector",
      sp.curved ? sp.type + " (curved)" : sp.type
    );
  }

  result.appendChild(dl);

  result.appendChild(el("h3", null, "Compatible case types"));
  const ul = el("ul", "chips");
  (phone.caseTypes || []).forEach((caseType) => {
    ul.appendChild(el("li", null, caseType));
  });
  result.appendChild(ul);

  const link = el(
    "a",
    "cta",
    "See the best cases for the " + phone.model + " ->"
  );
  link.href = phone.postUrl;
  link.rel = "noopener";
  result.appendChild(link);

  result.hidden = false;
}

async function init() {
  let phones;
  try {
    const res = await fetch("data/phones.json", { cache: "no-cache" });
    if (!res.ok) {
      throw new Error("HTTP " + res.status);
    }
    phones = (await res.json()).phones;
  } catch (err) {
    showError("Could not load the phone database. Please try again later.");
    console.error(err);
    return;
  }

  fillBrands(phones);
  fillModels(phones, "");

  brandSel.addEventListener("change", () => {
    fillModels(phones, brandSel.value);
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const phone = phones.find((p) => p.id === modelSel.value);
    if (phone) {
      render(phone);
    }
  });
}

init();

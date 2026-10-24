// House Assistant sidebar panel: one page for the whole house. Every module is a
// section with its own tabs (the former panels of the integrations). Plain web
// component without build step; uses only the hass object and the WebSocket commands.

import "./heating.js";
import "./shutter.js";
import "./meter.js";

const DOMAIN = "house_assistant";

const UI = {
  de: {
    title: "House Assistant",
    sections: { heating: "Heizung", shutter: "Rollos", meter: "Zähler" },
    noModules: "Es ist noch kein Modul eingeschaltet. Unter Einstellungen > Geräte & Dienste > House Assistant > Konfigurieren > Module lassen sie sich einschalten.",
    loadError: "Die Einstellungen konnten nicht geladen werden",
  },
  en: {
    title: "House Assistant",
    sections: { heating: "Heating", shutter: "Covers", meter: "Meters" },
    noModules: "No module is switched on yet. Switch them on under Settings > Devices & services > House Assistant > Configure > Modules.",
    loadError: "The settings could not be loaded",
  },
};

// section -> icon and the element that shows it
const SECTIONS = {
  heating: ["mdi:home-thermometer-outline", "house-assistant-heating-view"],
  shutter: ["mdi:window-shutter-auto", "house-assistant-shutter-view"],
  meter: ["mdi:counter", "house-assistant-meter-view"],
};

const esc = (value) =>
  String(value ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

class HouseAssistantPanel extends HTMLElement {
  constructor() {
    super();
    this._cfg = null;
    this._error = null;
    this._section = (location.hash || "").replace("#", "") || null;
    this._view = null;
    this.attachShadow({ mode: "open" });
    this.shadowRoot.addEventListener("click", (ev) => this._onClick(ev));
  }

  set hass(hass) {
    const first = !this._hass;
    this._hass = hass;
    if (first) this._load();
    if (this._view) this._view.hass = hass;
  }

  get hass() {
    return this._hass;
  }

  set narrow(value) {
    this._narrow = value;
    const btn = this.shadowRoot.querySelector(".menu");
    if (btn) btn.style.display = value ? "" : "none";
    if (this._view) this._view.narrow = value;
  }

  set panel(value) {
    this._panel = value;
  }

  get lang() {
    const language = this._hass?.locale?.language || this._hass?.language || "en";
    return language.startsWith("de") ? "de" : "en";
  }

  get ui() {
    return UI[this.lang];
  }

  async _load() {
    try {
      this._cfg = await this._hass.callWS({ type: `${DOMAIN}/config` });
      this._error = null;
    } catch (err) {
      this._error = err.message || String(err);
    }
    this._render();
  }

  get _sections() {
    return (this._cfg?.modules || []).filter((key) => SECTIONS[key]);
  }

  _render() {
    const ui = this.ui;
    const sections = this._sections;
    if (!sections.includes(this._section)) this._section = sections[0] || null;
    this.shadowRoot.innerHTML = `
      <style>${STYLE}</style>
      <div class="toolbar">
        <button class="menu icon-btn" data-action="menu" style="${this._narrow ? "" : "display:none"}"><ha-icon icon="mdi:menu"></ha-icon></button>
        <div class="title"><ha-icon icon="mdi:home-automation"></ha-icon>${esc(ui.title)}</div>
      </div>
      <div class="sections">
        ${sections
          .map(
            (key) =>
              `<button class="section ${this._section === key ? "active" : ""}" data-section="${key}"><ha-icon icon="${SECTIONS[key][0]}"></ha-icon><span>${esc(ui.sections[key] || key)}</span></button>`,
          )
          .join("")}
      </div>
      <div class="view"></div>`;
    const holder = this.shadowRoot.querySelector(".view");
    this._view = null;
    if (this._error) {
      holder.innerHTML = `<div class="card error">${esc(ui.loadError)}: ${esc(this._error)}</div>`;
      return;
    }
    if (!this._cfg) return;
    if (!this._section) {
      holder.innerHTML = `<div class="card">${esc(ui.noModules)}</div>`;
      return;
    }
    const view = document.createElement(SECTIONS[this._section][1]);
    view.narrow = this._narrow;
    view.panel = this._panel;
    view.hass = this._hass;
    holder.appendChild(view);
    this._view = view;
  }

  _onClick(ev) {
    const el = ev.target.closest("[data-section], [data-action]");
    if (!el) return;
    if (el.dataset.section) {
      this._section = el.dataset.section;
      history.replaceState(null, "", `#${this._section}`);
      this._render();
    } else if (el.dataset.action === "menu") {
      this.dispatchEvent(new Event("hass-toggle-menu", { bubbles: true, composed: true }));
    }
  }
}

const STYLE = `
:host { display:block; min-height:100vh; background:var(--primary-background-color); color:var(--primary-text-color); font-family:var(--paper-font-body1_-_font-family, Roboto, sans-serif); }
.toolbar { display:flex; align-items:center; height:56px; padding:0 12px; background:var(--app-header-background-color, var(--primary-color)); color:var(--app-header-text-color, #fff); gap:8px; }
.title { display:flex; align-items:center; gap:10px; font-size:20px; font-weight:400; }
.icon-btn { background:none; border:none; color:inherit; cursor:pointer; padding:8px; border-radius:50%; display:flex; }
.sections { display:flex; overflow-x:auto; background:var(--app-header-background-color, var(--primary-color)); padding:0 8px; scrollbar-width:none; }
.section { display:flex; align-items:center; gap:6px; background:none; border:none; color:var(--app-header-text-color, #fff); opacity:.75; padding:10px 14px; cursor:pointer; border-bottom:2px solid transparent; font-size:14px; white-space:nowrap; }
.section.active { opacity:1; border-bottom-color:var(--app-header-text-color, #fff); }
.section ha-icon { --mdc-icon-size:20px; }
.card { margin:16px; background:var(--ha-card-background, var(--card-background-color, #fff)); border-radius:var(--ha-card-border-radius, 12px); border:1px solid var(--divider-color, #e0e0e0); padding:16px; }
.card.error { color:var(--error-color); }
@media (max-width: 600px) {
  .section span { display:none; } .section.active span { display:inline; } .section { padding:10px 12px; }
}
`;

if (!customElements.get("house-assistant-panel")) {
  customElements.define("house-assistant-panel", HouseAssistantPanel);
}

// House section of the House Assistant panel: the rooms and windows every module builds
// on. Plain web component without build step; uses only the hass object and the
// WebSocket commands of the house. Field names and help texts come from the dialogs
// (labels.js), type, range and choices of every field from the integration.

import { HOUSE } from "./labels.js";
import { SECTION_TABS } from "./shared/style.js";

const WS = "house_assistant/house";

const UI = {
  de: {
    tabs: { rooms: "Räume", windows: "Fenster" },
    rooms: ["Räume", "Mit Temperatursensor bekommt ein Raum Heizung und Lüftungsempfehlung, mit Heizkreis auch ein Thermostat. Die Rollos seiner Fenster nehmen Raumtemperatur und Klimaanlage des Raums."],
    windows: ["Fenster", "Jedes Fenster einmal: mit Raum und Größe für die Heizung, mit Rollo für den Sonnenschutz. Ein Kontakt gehört zu genau einem Fenster."],
    columns: { name: "Name", area: "Bereich", temperature: "Temperatur", windows: "Fenster", heating: "Heizung", room: "Raum", size: "Größe", contacts: "Kontakte", cover: "Rollo" },
    newRoom: "Neuer Raum",
    newWindow: "Neues Fenster",
    add: "Hinzufügen",
    save: "Speichern",
    saved: "Gespeichert",
    cancel: "Abbrechen",
    delete: "Löschen",
    confirmRoom: "Raum wirklich löschen? Seine Fenster bleiben ohne Raum, gelernte Werte der Heizung gehen verloren.",
    confirmWindow: "Fenster wirklich löschen?",
    addValue: "Hinzufügen …",
    notFound: "nicht gefunden",
    none: "–",
    circuit: "Heizkreis",
    ventOnly: "nur Lüftung",
    noSensor: "ohne Sensor",
    open: "offen",
    closed: "zu",
    noRooms: "Noch keine Räume.",
    noWindows: "Noch keine Fenster.",
    windowsOfRoom: "Fenster dieses Raums",
    heatingHint: "Heizkreis, Sollwerte, Lüftung und Luftzug stehen im Bereich Heizung.",
    coverHint: "Sonnenschutz, Abend, Übersteuerung und die weiteren Einstellungen des Rollos stehen im Bereich Rollos.",
    loadError: "Die Einstellungen konnten nicht geladen werden",
    loading: "Lädt …",
    labels: {
      wall: ["Wand", "Wand des Hauses, in der das Fenster sitzt (von innen gesehen). Ohne Wand gilt die der Himmelsrichtung."],
      wall_position: ["Position an der Wand", "1 = ganz links, von innen durch die Wand nach draußen geschaut."],
    },
    walls: { front: "Vorderseite", right: "Rechte Seite", back: "Rückseite", left: "Linke Seite" },
  },
  en: {
    tabs: { rooms: "Rooms", windows: "Windows" },
    rooms: ["Rooms", "With a temperature sensor a room gets heating and ventilation advice, with a heating circuit also a thermostat. The covers of its windows take room temperature and air conditioner of the room."],
    windows: ["Windows", "Every window once: with room and size for the heating, with a cover for the sun protection. A contact belongs to one window only."],
    columns: { name: "Name", area: "Area", temperature: "Temperature", windows: "Windows", heating: "Heating", room: "Room", size: "Size", contacts: "Contacts", cover: "Cover" },
    newRoom: "New room",
    newWindow: "New window",
    add: "Add",
    save: "Save",
    saved: "Saved",
    cancel: "Cancel",
    delete: "Delete",
    confirmRoom: "Really delete this room? Its windows stay without a room, learned values of the heating are lost.",
    confirmWindow: "Really delete this window?",
    addValue: "Add …",
    notFound: "not found",
    none: "–",
    circuit: "Heating circuit",
    ventOnly: "ventilation only",
    noSensor: "no sensor",
    open: "open",
    closed: "closed",
    noRooms: "No rooms yet.",
    noWindows: "No windows yet.",
    windowsOfRoom: "Windows of this room",
    heatingHint: "Heating circuit, targets, ventilation and draft are in the heating section.",
    coverHint: "Sun protection, evening, override and the other settings of the cover are in the covers section.",
    loadError: "The settings could not be loaded",
    loading: "Loading …",
    labels: {
      wall: ["Wall", "Wall of the house the window sits in (seen from inside). Without a wall the one of the direction counts."],
      wall_position: ["Position on the wall", "1 = far left, looking out through the wall from inside."],
    },
    walls: { front: "Front", right: "Right side", back: "Back", left: "Left side" },
  },
};

const TABS = [
  ["rooms", "mdi:floor-plan"],
  ["windows", "mdi:window-closed-variant"],
];

const ROOM_FIELDS = ["area", "temperature_sensor", "humidity_sensor", "cooling_entity"];
const WINDOW_FIELDS = ["room", "size", "cover", "window_sensors", "tilt_sensors", "group", "wall", "wall_position"];

const esc = (value) =>
  String(value ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

const domainsOf = (spec) => {
  const domain = spec?.domain || spec?.filter?.flatMap?.((f) => [].concat(f.domain || [])) || [];
  return [].concat(domain);
};

class HouseAssistantHouseView extends HTMLElement {
  constructor() {
    super();
    this._cfg = null;
    this._error = null;
    this._tab = "rooms";
    this._edit = null;
    this.attachShadow({ mode: "open" });
    this.shadowRoot.addEventListener("click", (ev) => this._onClick(ev));
    this.shadowRoot.addEventListener("change", (ev) => this._onInput(ev, true));
    this.shadowRoot.addEventListener("input", (ev) => this._onInput(ev, false));
    this.shadowRoot.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" && ev.target.dataset?.add) {
        ev.preventDefault();
        this._addValue(ev.target);
      }
    });
    this.shadowRoot.addEventListener("value-changed", (ev) => this._onSelector(ev));
  }

  set hass(hass) {
    const first = !this._hass;
    this._hass = hass;
    if (first) {
      this._render();
      this._load();
      return;
    }
    // live values (temperatures, open windows) only while nothing is being edited
    if (!this._edit) this._renderContent();
  }

  get hass() {
    return this._hass;
  }

  set narrow(value) {
    this._narrow = value;
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

  get labels() {
    return HOUSE[this.lang] || HOUSE.en;
  }

  label(key) {
    const type = this._edit?.type || "room";
    return this.labels.fields[type][key] || this.ui.labels[key] || [key, ""];
  }

  async _load() {
    try {
      this._cfg = await this._hass.callWS({ type: `${WS}/config` });
      this._error = null;
    } catch (err) {
      this._error = err.message || String(err);
    }
    this._render();
  }

  _state(entityId) {
    return entityId ? this._hass?.states?.[entityId] : undefined;
  }

  _name(entityId) {
    const st = this._state(entityId);
    return st?.attributes?.friendly_name || entityId;
  }

  _areaName(areaId) {
    return areaId ? this._hass?.areas?.[areaId]?.name || areaId : "";
  }

  // ------------------------------------------------------------------ render

  _render() {
    this.shadowRoot.innerHTML = `
      <style>${STYLE}</style>
      <div class="tabs">
        ${TABS.map(([id, icon]) => `<button class="tab ${this._tab === id ? "active" : ""}" data-tab="${id}"><ha-icon icon="${icon}"></ha-icon><span>${esc(this.ui.tabs[id])}</span></button>`).join("")}
      </div>
      <div class="content"></div>
      <datalist id="dl-entities"></datalist>`;
    this._renderContent();
  }

  _renderContent() {
    const content = this.shadowRoot.querySelector(".content");
    if (!content) return;
    content.innerHTML = this._content();
    this._fillDatalist();
    this._upgradeSelectors();
  }

  _content() {
    const ui = this.ui;
    if (this._error) return `<div class="card error">${esc(ui.loadError)}: ${esc(this._error)}</div>`;
    if (!this._cfg) return `<div class="card muted">${esc(ui.loading)}</div>`;
    if (this._edit) return this._editor();
    return this._tab === "windows" ? this._windowsTab() : this._roomsTab();
  }

  _roomsTab() {
    const ui = this.ui;
    const cols = ui.columns;
    const rows = this._cfg.rooms
      .map((room) => {
        const d = room.data;
        const st = this._state(d.temperature_sensor);
        const temp = st && !["unknown", "unavailable"].includes(st.state) ? `${st.state} ${st.attributes?.unit_of_measurement || ""}` : ui.none;
        const heating = d.heater_switch ? ui.circuit : d.temperature_sensor ? ui.ventOnly : ui.noSensor;
        return `<tr data-edit-room="${esc(room.id)}">
          <td class="c-icon"><ha-icon icon="${d.heater_switch ? "mdi:home-thermometer-outline" : "mdi:floor-plan"}"></ha-icon></td>
          <td class="c-name"><div>${esc(room.title)}</div></td>
          <td class="hide-narrow">${esc(this._areaName(d.area) || ui.none)}</td>
          <td>${esc(temp)}</td>
          <td>${room.windows.length}</td>
          <td class="hide-narrow">${esc(heating)}</td></tr>`;
      })
      .join("");
    return `<div class="card">
      <h2>${esc(ui.rooms[0])}</h2><p class="desc">${esc(ui.rooms[1])}</p>
      ${rows ? `<div class="table-wrap"><table><thead><tr><th class="c-icon"></th><th>${esc(cols.name)}</th><th class="hide-narrow">${esc(cols.area)}</th><th>${esc(cols.temperature)}</th><th>${esc(cols.windows)}</th><th class="hide-narrow">${esc(cols.heating)}</th></tr></thead><tbody>${rows}</tbody></table></div>` : `<p class="muted">${esc(ui.noRooms)}</p>`}
      <div class="actions"><button class="btn primary" data-new="room"><ha-icon icon="mdi:plus"></ha-icon>${esc(ui.add)}</button></div>
    </div>`;
  }

  _windowsTab() {
    const ui = this.ui;
    const cols = ui.columns;
    const rooms = Object.fromEntries(this._cfg.rooms.map((r) => [r.id, r.title]));
    const rows = this._cfg.windows
      .map((win) => {
        const d = win.data;
        const contacts = d.window_sensors || [];
        const open = contacts.some((id) => this._state(id) && this._state(id).state !== "off" && this._state(id).state !== "closed");
        return `<tr data-edit-window="${esc(win.id)}">
          <td class="c-icon"><ha-icon icon="${d.cover ? "mdi:window-shutter" : open ? "mdi:window-open-variant" : "mdi:window-closed-variant"}"></ha-icon></td>
          <td class="c-name"><div>${esc(win.title)}</div></td>
          <td>${esc(rooms[d.room] || ui.none)}</td>
          <td class="hide-narrow">${esc(this.labels.sizes[d.size] || d.size)}</td>
          <td>${contacts.length ? `<span class="pill ${open ? "warn" : "ok"}">${esc(open ? ui.open : ui.closed)}</span>` : ui.none}</td>
          <td class="hide-narrow">${esc(d.cover ? this._name(d.cover) : ui.none)}</td></tr>`;
      })
      .join("");
    return `<div class="card">
      <h2>${esc(ui.windows[0])}</h2><p class="desc">${esc(ui.windows[1])}</p>
      ${rows ? `<div class="table-wrap"><table><thead><tr><th class="c-icon"></th><th>${esc(cols.name)}</th><th>${esc(cols.room)}</th><th class="hide-narrow">${esc(cols.size)}</th><th>${esc(cols.contacts)}</th><th class="hide-narrow">${esc(cols.cover)}</th></tr></thead><tbody>${rows}</tbody></table></div>` : `<p class="muted">${esc(ui.noWindows)}</p>`}
      <div class="actions"><button class="btn primary" data-new="window"><ha-icon icon="mdi:plus"></ha-icon>${esc(ui.add)}</button></div>
    </div>`;
  }

  _editor() {
    const ui = this.ui;
    const e = this._edit;
    const isRoom = e.type === "room";
    const specs = this._cfg.fields[e.type];
    const modules = this._cfg.modules || [];
    let keys = isRoom ? ROOM_FIELDS : WINDOW_FIELDS;
    keys = keys.filter((key) => key in specs);
    const fields = keys.map((key) => this._field(key, specs[key], e.data[key])).join("");
    let extra = "";
    if (isRoom && e.id) {
      const windows = this._cfg.windows.filter((w) => w.data.room === e.id);
      if (windows.length) {
        extra += `<h3>${esc(ui.windowsOfRoom)}</h3><div class="rows">${windows
          .map((w) => `<button class="row" data-edit-window="${esc(w.id)}"><ha-icon icon="${w.data.cover ? "mdi:window-shutter" : "mdi:window-closed-variant"}"></ha-icon><span class="grow">${esc(w.title)}</span><span class="muted">${esc(this.labels.sizes[w.data.size] || "")}</span></button>`)
          .join("")}</div>`;
      }
      if (modules.includes("heating")) extra += `<p class="desc hint">${esc(ui.heatingHint)}</p>`;
    }
    if (!isRoom && e.data.cover && modules.includes("shutter")) extra += `<p class="desc hint">${esc(ui.coverHint)}</p>`;
    const title = e.id ? e.title || e.originalTitle : isRoom ? ui.newRoom : ui.newWindow;
    return `<div class="card" data-card="edit">
      <h2><button class="icon-btn" data-action="close"><ha-icon icon="mdi:arrow-left"></ha-icon></button>
        <ha-icon icon="${isRoom ? "mdi:floor-plan" : "mdi:window-closed-variant"}"></ha-icon>${esc(title)}</h2>
      <div class="fields">${this._field("name", { selector: "text" }, e.title)}${fields}</div>
      ${extra}
      <div class="actions"><span class="msg"></span>
        ${e.id ? `<button class="btn danger" data-action="delete">${esc(ui.delete)}</button>` : ""}
        <span class="grow"></span>
        <button class="btn" data-action="close">${esc(ui.cancel)}</button>
        <button class="btn primary" data-action="save">${esc(ui.save)}</button></div>
    </div>`;
  }

  _field(key, spec, value) {
    const ui = this.ui;
    const [name, help] = this.label(key);
    const kind = spec?.selector || "text";
    const helpHtml = help ? `<small>${esc(help)}</small>` : "";
    const attrs = (type) => `data-k="${key}" data-type="${type}"`;
    if ((kind === "entity" || kind === "area") && customElements.get("ha-selector")) {
      // Home Assistant's own pickers (names, areas, filters) when available
      this._selectors = this._selectors || new Map();
      this._selectors.set(key, { spec, value, name });
      return `<div class="field"><ha-selector ${attrs("selector")}></ha-selector>${helpHtml}</div>`;
    }
    switch (kind) {
      case "number":
        return `<label class="field"><span class="lbl">${esc(name)}</span><span class="with-unit">
          <input type="number" ${attrs("number")} value="${esc(value ?? "")}" min="${spec.min ?? ""}" max="${spec.max ?? ""}" step="${spec.step ?? "any"}">
          ${spec.unit_of_measurement ? `<span class="unit">${esc(spec.unit_of_measurement)}</span>` : ""}</span>${helpHtml}</label>`;
      case "select": {
        const texts = spec.translation_key === "window_size" ? this.labels.sizes : key === "wall" ? ui.walls : {};
        const options = (spec.options || []).map((o) => (typeof o === "object" ? [o.value, o.label] : [o, texts[o] || o]));
        const empty = spec.translation_key ? "" : `<option value=""></option>`;
        return `<label class="field"><span class="lbl">${esc(name)}</span><select ${attrs("text")}>${empty}
          ${options.map(([v, label]) => `<option value="${esc(v)}" ${v === value ? "selected" : ""}>${esc(label)}</option>`).join("")}
          </select>${helpHtml}</label>`;
      }
      case "area": {
        const areas = Object.values(this._hass?.areas || {});
        return `<label class="field"><span class="lbl">${esc(name)}</span><select ${attrs("text")}><option value=""></option>
          ${areas.map((a) => `<option value="${esc(a.area_id)}" ${a.area_id === value ? "selected" : ""}>${esc(a.name)}</option>`).join("")}
          </select>${helpHtml}</label>`;
      }
      case "entity": {
        if (spec.multiple) {
          const list = Array.isArray(value) ? value : [];
          const chips = list
            .map((item, i) => {
              const st = this._state(item);
              return `<span class="chip ${st ? "" : "bad"}" title="${esc(item)}">${esc(st ? this._name(item) : item)}<button class="chip-btn" data-remove="${i}" ${attrs("entities")}>✕</button></span>`;
            })
            .join("");
          return `<div class="field"><span class="lbl">${esc(name)}</span><div class="chips">${chips}</div>
            <input type="text" list="dl-entities" data-add="1" ${attrs("entities")} data-domains="${esc(domainsOf(spec).join(","))}" placeholder="${esc(ui.addValue)}" autocomplete="off">${helpHtml}</div>`;
        }
        const st = value ? this._state(value) : null;
        const hint = value ? (st ? this._name(value) : `⚠ ${ui.notFound}`) : "";
        return `<label class="field"><span class="lbl">${esc(name)}</span>
          <input type="text" list="dl-entities" ${attrs("entity")} data-domains="${esc(domainsOf(spec).join(","))}" value="${esc(value ?? "")}" placeholder="${esc(domainsOf(spec)[0] || "entity")}.…" autocomplete="off">
          <span class="entity-hint ${value && !st ? "bad" : ""}">${esc(hint)}</span>${helpHtml}</label>`;
      }
      default:
        return `<label class="field"><span class="lbl">${esc(name)}</span><input type="text" ${attrs("text")} value="${esc(value ?? "")}">${helpHtml}</label>`;
    }
  }

  _fillDatalist() {
    const list = this.shadowRoot.getElementById("dl-entities");
    if (!list || !this._edit) return;
    list.innerHTML = Object.keys(this._hass?.states || {})
      .sort()
      .map((id) => `<option value="${esc(id)}">${esc(this._name(id))}</option>`)
      .join("");
  }

  _upgradeSelectors() {
    for (const el of this.shadowRoot.querySelectorAll("ha-selector[data-k]")) {
      const field = this._selectors?.get(el.dataset.k);
      if (!field) continue;
      const { selector, ...config } = field.spec || {};
      el.hass = this._hass;
      el.selector = { [selector || "entity"]: config };
      el.label = field.name;
      el.value = field.value ?? (config.multiple ? [] : "");
      el.required = false;
    }
  }

  // ------------------------------------------------------------------ events

  _set(key, value) {
    const e = this._edit;
    if (!e) return;
    if (key === "name") e.title = value;
    else if (value === null || value === "" || (Array.isArray(value) && !value.length)) delete e.data[key];
    else e.data[key] = value;
  }

  _onSelector(ev) {
    const el = ev.target.closest?.("ha-selector[data-k]");
    if (!el) return;
    this._set(el.dataset.k, ev.detail?.value);
    if (el.dataset.k === "cover") this._renderContent();
  }

  _onInput(ev, isChange) {
    const el = ev.target;
    const key = el.dataset?.k;
    if (!key || el.dataset.add) return;
    const type = el.dataset.type;
    if (type === "entities" || type === "selector") return;
    let value = el.value;
    if (type === "number") value = el.value === "" ? null : Number(el.value);
    if (type === "entity") {
      const hint = el.parentElement.querySelector(".entity-hint");
      if (hint) {
        const st = value ? this._state(value) : null;
        hint.textContent = value ? (st ? this._name(value) : `⚠ ${this.ui.notFound}`) : "";
        hint.classList.toggle("bad", !!value && !st);
      }
    }
    this._set(key, value);
    if (isChange && key === "cover") this._renderContent();
  }

  _addValue(input) {
    const value = input.value.trim();
    if (!value) return;
    const key = input.dataset.k;
    const list = [...(this._edit.data[key] || [])];
    if (!list.includes(value)) list.push(value);
    this._set(key, list);
    this._renderContent();
    this.shadowRoot.querySelector(`input[data-add][data-k="${key}"]`)?.focus();
  }

  _onClick(ev) {
    const el = ev.target.closest("[data-tab], [data-new], [data-edit-room], [data-edit-window], [data-action], [data-remove]");
    if (!el) return;
    if (el.dataset.tab) {
      this._tab = el.dataset.tab;
      this._edit = null;
      this._render();
    } else if (el.dataset.new) {
      this._edit = { type: el.dataset.new, id: null, title: "", data: el.dataset.new === "window" ? { size: "medium" } : {} };
      this._renderContent();
    } else if (el.dataset.editRoom || el.dataset.editWindow) {
      const isRoom = !!el.dataset.editRoom;
      const item = (isRoom ? this._cfg.rooms : this._cfg.windows).find((x) => x.id === (el.dataset.editRoom || el.dataset.editWindow));
      if (!item) return;
      this._edit = { type: isRoom ? "room" : "window", id: item.id, title: item.title, originalTitle: item.title, data: JSON.parse(JSON.stringify(item.data)) };
      this._renderContent();
    } else if (el.dataset.remove !== undefined) {
      const key = el.dataset.k;
      const list = [...(this._edit.data[key] || [])];
      list.splice(Number(el.dataset.remove), 1);
      this._set(key, list);
      this._renderContent();
    } else if (el.dataset.action === "close") {
      this._edit = null;
      this._renderContent();
    } else if (el.dataset.action === "save") {
      this._save();
    } else if (el.dataset.action === "delete") {
      this._delete();
    }
  }

  _message(text, bad) {
    const msg = this.shadowRoot.querySelector(".msg");
    if (!msg) return;
    msg.textContent = text;
    msg.classList.toggle("bad", !!bad);
  }

  _errorText(err) {
    const [code, field] = String(err?.message || err).split(":");
    const text = this.labels.errors[code] || code;
    return field ? `${this.label(field)[0]}: ${text}` : text;
  }

  async _save() {
    const e = this._edit;
    // a pending entry of a list field counts as well
    for (const input of this.shadowRoot.querySelectorAll("input[data-add]")) if (input.value.trim()) this._addValue(input);
    try {
      const result = await this._hass.callWS({ type: `${WS}/save`, subentry_type: e.type, ...(e.id ? { subentry_id: e.id } : {}), title: e.title || "", data: e.data });
      this._cfg = result.config;
      this._edit = null;
      this._renderContent();
    } catch (err) {
      this._message(this._errorText(err), true);
    }
  }

  async _delete() {
    const e = this._edit;
    if (!e?.id || !confirm(e.type === "room" ? this.ui.confirmRoom : this.ui.confirmWindow)) return;
    try {
      const result = await this._hass.callWS({ type: `${WS}/delete`, subentry_id: e.id });
      this._cfg = result.config;
      this._edit = null;
      this._renderContent();
    } catch (err) {
      this._message(this._errorText(err), true);
    }
  }
}

const STYLE = `
:host { display:block; min-height:calc(100vh - 104px); overflow-x:hidden; background:var(--primary-background-color); color:var(--primary-text-color); font-family:var(--paper-font-body1_-_font-family, Roboto, sans-serif); }
* { box-sizing:border-box; }
${SECTION_TABS}
.content { padding:16px; max-width:1200px; margin:0 auto; }
.card { min-width:0; overflow-wrap:anywhere; background:var(--ha-card-background, var(--card-background-color, #fff)); border-radius:var(--ha-card-border-radius, 12px); border:1px solid var(--divider-color, #e0e0e0); padding:16px; box-shadow:var(--ha-card-box-shadow, none); }
.card.error { color:var(--error-color); }
h2 { display:flex; align-items:center; gap:10px; margin:0 0 4px; font-size:18px; font-weight:500; }
h2 ha-icon { color:var(--state-icon-color, var(--primary-color)); }
h3 { margin:20px 0 4px; font-size:15px; font-weight:500; }
.desc { margin:0 0 12px; color:var(--secondary-text-color); font-size:14px; }
.hint { margin-top:16px; }
.fields { display:grid; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); gap:12px 20px; margin-top:8px; }
.field { display:flex; flex-direction:column; gap:4px; font-size:14px; }
.lbl { font-weight:500; }
small { color:var(--secondary-text-color); font-size:12px; line-height:1.3; }
input[type=text], input[type=number], select {
  font:inherit; color:var(--primary-text-color); background:var(--input-fill-color, var(--secondary-background-color, #f5f5f5));
  border:1px solid var(--divider-color, #ccc); border-radius:8px; padding:8px 10px; width:100%; }
input:focus, select:focus { outline:2px solid var(--primary-color); outline-offset:-1px; }
.with-unit { display:flex; align-items:center; gap:6px; }
.unit { color:var(--secondary-text-color); min-width:24px; white-space:nowrap; }
.entity-hint { font-size:12px; color:var(--secondary-text-color); min-height:14px; }
.entity-hint.bad, .msg.bad { color:var(--error-color, #db4437); }
.chips { display:flex; flex-wrap:wrap; gap:6px; }
.chip { display:inline-flex; align-items:center; gap:4px; border-radius:14px; padding:2px 4px 2px 10px; font-size:13px; background:var(--secondary-background-color, #eee); }
.chip.bad { color:var(--error-color, #db4437); }
.chip-btn { background:none; border:none; cursor:pointer; color:inherit; padding:0 4px; }
.actions { display:flex; align-items:center; justify-content:flex-end; gap:8px; margin-top:16px; flex-wrap:wrap; }
.msg { margin-right:auto; font-size:13px; color:var(--secondary-text-color); }
.grow { flex:1; }
.btn { display:inline-flex; align-items:center; gap:6px; font:inherit; font-weight:500; border-radius:18px; padding:8px 16px; cursor:pointer; border:1px solid var(--divider-color); background:none; color:var(--primary-color); }
.btn ha-icon { --mdc-icon-size:18px; }
.btn.primary { background:var(--primary-color); color:var(--text-primary-color, #fff); border-color:var(--primary-color); }
.btn.danger { color:var(--error-color, #db4437); border-color:var(--error-color, #db4437); }
.icon-btn { background:none; border:none; color:inherit; cursor:pointer; padding:4px; display:inline-flex; }
.rows { display:flex; flex-direction:column; }
.row { display:flex; align-items:center; gap:10px; padding:8px 4px; border-bottom:1px solid var(--divider-color); font:inherit; font-size:14px; color:var(--primary-text-color); background:none; border-left:none; border-right:none; border-top:none; text-align:left; width:100%; cursor:pointer; }
.row:last-child { border-bottom:none; }
.muted { color:var(--secondary-text-color); }
.pill { display:inline-block; border-radius:12px; padding:2px 10px; font-size:12px; background:var(--secondary-background-color, #eee); white-space:nowrap; }
.pill.ok { background:rgba(67,160,71,.15); color:var(--success-color, #2e7d32); }
.pill.warn { background:rgba(255,166,0,.18); color:var(--warning-color, #b26a00); }
.table-wrap { width:100%; overflow-x:auto; }
table { width:100%; border-collapse:collapse; font-size:14px; table-layout:fixed; }
th.c-icon { width:40px; }
th { white-space:nowrap; overflow:hidden; text-overflow:ellipsis; text-align:left; font-weight:500; color:var(--secondary-text-color); padding:6px 8px; border-bottom:1px solid var(--divider-color); }
td { padding:8px; border-bottom:1px solid var(--divider-color); vertical-align:middle; }
tbody tr { cursor:pointer; }
tbody tr:hover { background:var(--secondary-background-color, #f5f5f5); }
@media (max-width: 700px) {
  .hide-narrow { display:none; } .content { padding:8px; }
  .tab span { display:none; } .tab.active span { display:inline; } .tab { padding:10px 12px; }
  .fields { grid-template-columns:1fr; } th.c-icon { width:32px; } td { padding:8px 4px; } .card { padding:12px; }
}
`;

if (!customElements.get("house-assistant-house-view")) {
  customElements.define("house-assistant-house-view", HouseAssistantHouseView);
}

// Defines the custom elements of House Assistant so they stay known to the frontend.
//
// The Home Assistant frontend loads a polyfill for scoped custom element registries on
// demand (e.g. with the media control card) and then replaces window.customElements by
// a new registry. That registry only knows the elements defined through it: a card
// defined before the swap is unknown afterwards and the dashboard shows "Configuration
// error" (seen after reloading a view with a media control card). So every element is
// defined again in the new registry as soon as window.customElements changes.

const elements = new Map();
let registry = window.customElements;
let timer = null;

const native = (reg) => String(reg.define).includes("[native code]");

function add(reg, name, cls) {
  if (reg.get(name)) return false;
  try {
    reg.define(name, cls);
    return true;
  } catch (err) {
    // the name is taken already (e.g. a second copy of a file under another version)
    return false;
  }
}

function watch() {
  // the polyfill replaces the registry once; with it in place already there is nothing to wait for
  if (timer || !native(registry)) return;
  timer = setInterval(() => {
    if (window.customElements === registry) return;
    registry = window.customElements;
    for (const [name, cls] of elements) add(registry, name, cls);
    if (!native(registry)) {
      clearInterval(timer);
      timer = null;
    }
  }, 200);
}

// Defines the element; true if it was not defined before (then register the card picker entry).
export function defineElement(name, cls) {
  if (!elements.has(name)) elements.set(name, cls);
  const added = add(window.customElements, name, cls);
  watch();
  return added;
}

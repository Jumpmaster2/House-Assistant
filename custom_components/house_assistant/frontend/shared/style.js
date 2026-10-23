// Styles shared by the sections of the House Assistant panel.

// Tabs of a section: below the sections of the panel, so they look quieter.
export const SECTION_TABS = `
.tabs { display:flex; overflow-x:auto; background:var(--card-background-color, #fff); border-bottom:1px solid var(--divider-color, #e0e0e0); padding:0 8px; scrollbar-width:none; }
.tab { display:flex; align-items:center; gap:6px; background:none; border:none; color:var(--primary-text-color); opacity:.7; padding:10px 14px; cursor:pointer; border-bottom:2px solid transparent; font-size:14px; white-space:nowrap; }
.tab.active { opacity:1; color:var(--primary-color); border-bottom-color:var(--primary-color); }
.tab ha-icon { --mdc-icon-size:20px; }
`;

// Settings of the house that win over the same settings of a module (SHARED_KEYS in
// const.py). A module shows them as a note instead of its own field, so nothing is set
// twice; without a value in the house the field of the module stays.

export const SHARED_KEYS = [
  "outdoor_temperature",
  "outdoor_humidity",
  "weather",
  "language",
  "notify_services",
  "workday_entity",
  "weekend_days",
  "house_azimuth",
  "house_width",
  "house_depth",
  "draft_reach",
  "vacation_entities",
  "return_entity",
];

// the house sets the key (the backend only sends the settings that are set)
export const fromHouse = (house, key) => SHARED_KEYS.includes(key) && house != null && key in house;

export const HOUSE_NOTE = {
  de: ["Aus dem Haus", "Gilt für alle Module, ändern unter Haus › Einstellungen."],
  en: ["From the house", "Applies to every module, change under House › Settings."],
};

// "label: value" pairs of the keys the house sets, for the note of a settings card
export function houseValues(house, keys, label) {
  return keys
    .filter((key) => fromHouse(house, key))
    .map((key) => {
      const value = house[key];
      return [label(key)[0], Array.isArray(value) ? value.join(", ") : String(value)];
    });
}

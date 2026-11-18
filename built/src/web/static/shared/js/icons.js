/**
 * MllyMed — Markaziy ikonka kutubxonasi (Lucide-uslub, 24px stroke-grid)
 * Emoji ishlatish taqiqlangan — shu yerdan inline SVG olinadi.
 * Foydalanish: icon('search', 18)  → <svg ...>
 */
(function () {
  const PATHS = {
    search: '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    pill: '<path d="M10.5 20.5a7.07 7.07 0 0 1-10-10l6-6a7.07 7.07 0 0 1 10 10l-6 6Z"/><path d="m8.5 8.5 7 7"/>',
    capsule: '<rect x="3.5" y="8.5" width="17" height="7" rx="3.5" transform="rotate(-45 12 12)"/><line x1="8.8" y1="15.2" x2="15.2" y2="8.8"/>',
    stethoscope: '<path d="M4.8 2.3A.3.3 0 1 0 5.3 4H5a7 7 0 0 0 7 7 7 7 0 0 0 7-7h-.3A.3.3 0 1 0 19.2 2.3"/><path d="M8 4v6a4 4 0 0 0 8 0V4"/><path d="M12 14v2a6 6 0 0 0 6 6 6 6 0 0 0 6-6v-1.5"/><circle cx="22" cy="12.5" r="1.6"/>',
    'heart-pulse': '<path d="M19.5 13.6 12 21l-7.5-7.4A5 5 0 0 1 12 6.3a5 5 0 0 1 7.5 7.3Z"/><path d="M3.5 12h4l1.5-3 2.5 5 2-4 1.5 2h6"/>',
    heart: '<path d="M19.5 13.6 12 21l-7.5-7.4A5 5 0 0 1 12 6.3a5 5 0 0 1 7.5 7.3Z"/>',
    shield: '<path d="M12 2.5 4.5 6v6c0 4.8 3.2 9.3 7.5 10.5 4.3-1.2 7.5-5.7 7.5-10.5V6L12 2.5Z"/><path d="m9.5 12 2 2 3.5-4"/>',
    'file-text': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6Z"/><path d="M14 2v6h6"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/><line x1="9" y1="9" x2="10.5" y2="9"/>',
    'clipboard-check': '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 13.5 2 2 4-4.5"/>',
    building: '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 21v-4h6v4"/><path d="M8 7h.01M12 7h.01M16 7h.01M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01"/>',
    factory: '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1M12 18h1M7 18h1"/>',
    store: '<path d="M3 9l1.7-5.2A1.6 1.6 0 0 1 6.2 2.7h11.6a1.6 1.6 0 0 1 1.5 1.1L21 9"/><path d="M4 9v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9"/><path d="M9 21v-6h6v6"/><path d="M3 9h18"/>',
    globe: '<circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19"/><path d="M12 2.5a15 15 0 0 1 0 19 15 15 0 0 1 0-19Z"/><path d="M12 2.5a15 15 0 0 0 0 19"/>',
    flag: '<path d="M4 21V4"/><path d="M4 5c2-1.4 4.2-1.8 6.5-.8L14 6.4a9 9 0 0 0 6-1V13a9 9 0 0 1-6 1l-3.5-2.2A12 12 0 0 0 4 14"/>',
    check: '<polyline points="20 6 9 17 4 10"/>',
    'check-circle': '<circle cx="12" cy="12" r="9.5"/><path d="m8.5 12.2 2.4 2.4 4.6-5.4"/>',
    'alert-triangle': '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><line x1="12" y1="9.5" x2="12" y2="13.5"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    'x-circle': '<circle cx="12" cy="12" r="9.5"/><line x1="9" y1="9" x2="15" y2="15"/><line x1="15" y1="9" x2="9" y2="15"/>',
    x: '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    tag: '<path d="M12.6 2.6a2 2 0 0 0-1.4-.6H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l9.7 9.7a2 2 0 0 0 2.8 0l7.2-7.2a2 2 0 0 0 0-2.8l-9.7-9.7Z"/><circle cx="7.5" cy="7.5" r="1.4"/>',
    package: '<path d="M21 8.2v7.6a2 2 0 0 1-1 1.7l-7 4a2 2 0 0 1-2 0l-7-4a2 2 0 0 1-1-1.7V8.2a2 2 0 0 1 1-1.7l7-4a2 2 0 0 1 2 0l7 4a2 2 0 0 1 1 1.7Z"/><path d="M3.3 7.3 12 12l8.7-4.7"/><path d="M12 22V12"/>',
    lock: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    calendar: '<rect x="3" y="4" width="18" height="17" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    bell: '<path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
    user: '<circle cx="12" cy="8" r="4.5"/><path d="M4.5 21a7.5 7.5 0 0 1 15 0"/>',
    clock: '<circle cx="12" cy="12" r="9.5"/><polyline points="12 7 12 12 15.5 14"/>',
    'arrow-right': '<line x1="4" y1="12" x2="20" y2="12"/><polyline points="13 5 20 12 13 19"/>',
    'arrow-up-right': '<line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/>',
    'chevron-right': '<polyline points="9 18 15 12 9 6"/>',
    'chevron-left': '<polyline points="15 18 9 12 15 6"/>',
    sparkles: '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3Z"/><path d="M19 14l.8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8L19 14Z"/>',
    activity: '<polyline points="22 12 16.5 12 14 6l-4.5 11L7 12H2"/>',
    truck: '<path d="M1 3h15v13H1z"/><path d="M16 8h4l3 3v5h-7"/><circle cx="5.5" cy="18.5" r="2"/><circle cx="18.5" cy="18.5" r="2"/>',
    info: '<circle cx="12" cy="12" r="9.5"/><line x1="12" y1="11" x2="12" y2="16"/><line x1="12" y1="7.5" x2="12.01" y2="7.5"/>',
    phone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.13 1 .4 2 .8 2.8a2 2 0 0 1-.5 2.4L8 11.6a16 16 0 0 0 6 6l2.7-1.4a2 2 0 0 1 2.4.5c.9.4 1.9.7 2.9.8a2 2 0 0 1 2 2Z"/>',
    building2: '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18"/><path d="M2 22h20"/><path d="M9.5 7h1M13.5 7h1M9.5 11h1M13.5 11h1M9.5 15h1M13.5 15h1"/>',
    star: '<polygon points="12 2 15.1 8.6 22.4 9.6 17.2 14.7 18.4 22 12 18.6 5.6 22 6.8 14.7 1.6 9.6 8.9 8.6 12 2"/>',
    external: '<path d="M18 13v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>',
    wifi: '<path d="M5 12.5a10 10 0 0 1 14 0"/><path d="M8.5 16a5 5 0 0 1 7 0"/><line x1="12" y1="19.5" x2="12.01" y2="19.5"/><path d="M1.5 9a15 15 0 0 1 21 0"/>',
  };

  window.icon = function (name, size, strokeWidth) {
    const body = PATHS[name];
    if (!body) return '';
    const s = size || 18;
    const w = strokeWidth || 2;
    return '<svg width="' + s + '" height="' + s + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="' + w + '" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>';
  };
})();

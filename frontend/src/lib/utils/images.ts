function pickPalette(seed: string) {
  const palettes = [
    ["#E56C2E", "#F4C15D", "#FFF2D9"],
    ["#3D8C68", "#A7D7B5", "#EEF8F0"],
    ["#B84D3C", "#F1B075", "#FFF1E6"],
    ["#5A6FD6", "#9AC5F4", "#EEF3FF"],
    ["#7A5C3D", "#D9B183", "#FBF1E3"],
  ];
  let hash = 0;
  for (let index = 0; index < seed.length; index += 1) {
    hash = (hash + seed.charCodeAt(index) * (index + 3)) % palettes.length;
  }
  return palettes[hash];
}

function createPlaceholder(recipeName: string, label: string) {
  const [accent, soft, base] = pickPalette(`${recipeName}-${label}`);
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="800" height="520" viewBox="0 0 800 520">
      <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="${accent}" />
          <stop offset="100%" stop-color="${soft}" />
        </linearGradient>
      </defs>
      <rect width="800" height="520" rx="36" fill="url(#bg)" />
      <circle cx="660" cy="100" r="120" fill="${base}" fill-opacity="0.46" />
      <circle cx="120" cy="430" r="150" fill="${base}" fill-opacity="0.28" />
      <rect x="50" y="54" width="156" height="42" rx="21" fill="${base}" fill-opacity="0.88" />
      <text x="78" y="81" font-size="22" font-family="Arial, PingFang SC, Microsoft YaHei, sans-serif" fill="${accent}">${label}</text>
      <text x="52" y="262" font-size="54" font-weight="700" font-family="Arial, PingFang SC, Microsoft YaHei, sans-serif" fill="white">${recipeName}</text>
      <text x="54" y="304" font-size="24" font-family="Arial, PingFang SC, Microsoft YaHei, sans-serif" fill="rgba(255,255,255,0.88)">Meituan Cloud Fridge Demo</text>
      <rect x="54" y="344" width="240" height="12" rx="6" fill="rgba(255,255,255,0.75)" />
      <rect x="54" y="370" width="184" height="12" rx="6" fill="rgba(255,255,255,0.55)" />
    </svg>
  `;
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

export function resolveRecipeImage(coverImage: string, recipeName: string, label = "Tonight") {
  if (coverImage && /^https?:\/\//.test(coverImage)) {
    return coverImage;
  }
  return createPlaceholder(recipeName, label);
}


(function () {
	/*
	 * Theme strategy:
	 * - Choose mode from local clock on every page load.
	 * - Keep dark/light palettes separate so each mode can rotate colors independently.
	 * - Let users toggle manually, but do not persist mode overrides across reloads.
	 */
	const PAIRS = [
		{ fg: "#D0D1D4", bg: "#0D121F" },
		{ fg: "#504F4F", bg: "#E2E2E2" },
		{ fg: "#18185E", bg: "#C1B676" },
		{ fg: "#DEE6FF", bg: "#143199" },
		{ fg: "#3D3D3D", bg: "#96DCED" },
		{ fg: "#E48244", bg: "#442C25" },
		{ fg: "#FF4445", bg: "#222222" },
		{ fg: "#0B1743", bg: "#FFB55E" },
		{ fg: "#F9C350", bg: "#303328" },
		{ fg: "#EF9E40", bg: "#2328A0" },
		{ fg: "#452121", bg: "#FF9E5A" },
		{ fg: "#DBDBDB", bg: "#2F2F2F" },
		{ fg: "#222222", bg: "#FFA6A6" },
		{ fg: "#222222", bg: "#CAD9E5" },
		{ fg: "#0AEB9A", bg: "#353F54" }
	];

	const INDEX_KEY_PREFIX = "themeIndex:";
	const DARK_BG_THRESHOLD = 0.45;
	const BG_LIGHTEN_DARK = 0.16;
	const BG_LIGHTEN_LIGHT = 0.32;
	const LIGHT_START_MINUTES = (10 * 60) + 1;
	const LIGHT_END_MINUTES = 18 * 60;

	const root = document.documentElement;
	const style = root.style;
	const themeToggle = document.getElementById("theme-toggle");

	function hexToRgb(hex) {
		const cleanHex = hex.replace("#", "");
		const r = Number.parseInt(cleanHex.slice(0, 2), 16);
		const g = Number.parseInt(cleanHex.slice(2, 4), 16);
		const b = Number.parseInt(cleanHex.slice(4, 6), 16);
		return { r, g, b };
	}

	function toLinear(channel) {
		const normalized = channel / 255;
		if (normalized <= 0.03928) {
			return normalized / 12.92;
		}
		return ((normalized + 0.055) / 1.055) ** 2.4;
	}

	function luminance(hex) {
		const { r, g, b } = hexToRgb(hex);
		return (0.2126 * toLinear(r)) + (0.7152 * toLinear(g)) + (0.0722 * toLinear(b));
	}

	function channelToHex(value) {
		return value.toString(16).padStart(2, "0");
	}

	function lightenHex(hex, ratio) {
		const { r, g, b } = hexToRgb(hex);
		const nr = Math.round(r + ((255 - r) * ratio));
		const ng = Math.round(g + ((255 - g) * ratio));
		const nb = Math.round(b + ((255 - b) * ratio));
		return `#${channelToHex(nr)}${channelToHex(ng)}${channelToHex(nb)}`;
	}

	const darkPairs = PAIRS.filter((pair) => luminance(pair.bg) < DARK_BG_THRESHOLD);
	const lightPairs = PAIRS.filter((pair) => luminance(pair.bg) >= DARK_BG_THRESHOLD);

	function getModePairs(mode) {
		if (mode === "dark" && darkPairs.length) {
			return darkPairs;
		}
		if (mode === "light" && lightPairs.length) {
			return lightPairs;
		}
		return PAIRS;
	}

	function nextPairForMode(mode) {
		const modePairs = getModePairs(mode);
		const key = `${INDEX_KEY_PREFIX}${mode}`;
		const last = Number(localStorage.getItem(key));
		/* Keep one cursor per mode so switching back does not always repeat the same pair. */
		const idx = Number.isFinite(last) ? (last + 1) % modePairs.length : 0;
		localStorage.setItem(key, String(idx));
		return modePairs[idx];
	}

	function applyTheme(mode, pair) {
		const isLightPair = luminance(pair.bg) >= DARK_BG_THRESHOLD;
		/* Raw palette backgrounds are a bit too saturated; lighten slightly for reading comfort. */
		const lightenRatio = isLightPair ? BG_LIGHTEN_LIGHT : BG_LIGHTEN_DARK;
		const bg = lightenHex(pair.bg, lightenRatio);

		style.setProperty("--fg", pair.fg);
		style.setProperty("--bg", bg);
		style.setProperty("--link", pair.fg);
		root.dataset.themeMode = mode;
		if (themeToggle) {
			const oppositeMode = mode === "dark" ? "light" : "dark";
			themeToggle.setAttribute("aria-label", `Switch to ${oppositeMode} mode`);
			themeToggle.title = `Switch to ${oppositeMode} mode`;
		}
	}

	function getModeForTime(now = new Date()) {
		const minutesFromMidnight = (now.getHours() * 60) + now.getMinutes();
		/*
		 * Boundaries are explicit:
		 * - 10:00 is still dark.
		 * - 10:01 starts light mode.
		 * - 18:00 is still light.
		 * - 18:01 returns to dark mode.
		 */
		if (minutesFromMidnight >= LIGHT_START_MINUTES && minutesFromMidnight <= LIGHT_END_MINUTES) {
			return "light";
		}
		return "dark";
	}

	function getInitialMode() {
		/* Intentional: schedule wins over system preference and past sessions. */
		return getModeForTime();
	}

	let currentMode = getInitialMode();
	applyTheme(currentMode, nextPairForMode(currentMode));

	if (themeToggle) {
		themeToggle.addEventListener("click", () => {
			currentMode = currentMode === "dark" ? "light" : "dark";
			applyTheme(currentMode, nextPairForMode(currentMode));
		});
	}
})();


(function () {
	// Exact pairs (text → foreground, background) as found
	  const PAIRS = [
		  { fg: "#D0D1D4", bg: "#0D121F" },
		  { fg: "#504F4F", bg: "#E2E2E2" },
		  { fg: "#EBADCB", bg: "#4D1A28" },
		  { fg: "#18185E", bg: "#C1B676" },
		  { fg: "#DEE6FF", bg: "#143199" },
		  { fg: "#333032", bg: "#93935F" },
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
  
	  // Remember last index and advance so each reload shows a different pair
	  const KEY = "themeIndex";
	  const last = Number(localStorage.getItem(KEY));
	  const idx = Number.isFinite(last) ? (last + 1) % PAIRS.length : 0;
	  localStorage.setItem(KEY, String(idx));
  
	  const { fg, bg } = PAIRS[idx];
  
	  // Set CSS variables once; the CSS handles everything else
	  const s = document.documentElement.style;
	  s.setProperty("--fg", fg);
	  s.setProperty("--bg", bg);
	  s.setProperty("--link", fg); // links = text (no adjustments)
  })();
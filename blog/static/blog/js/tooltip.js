
(() => {
  // If Popover API isn't supported, do nothing (you can fallback to title=... if you want).
  const supportsPopover =
    typeof HTMLElement !== "undefined" &&
    "showPopover" in HTMLElement.prototype &&
    "hidePopover" in HTMLElement.prototype;

  if (!supportsPopover) return;

  const GAP_PX = 8;          // Space between anchor and popover
  const HIDE_DELAY_MS = 80;  // Prevents flicker moving mouse from link to popover

  document.querySelectorAll("li.hasPopover[data-popover-id]").forEach((li) => {
    const anchor = li.querySelector("a");
    const popoverId = li.getAttribute("data-popover-id");
    const pop = document.getElementById(popoverId);

    if (!anchor || !pop) return;

    let hideTimer = null;

    // Keep this tiny and defensive: showPopover/hidePopover throw if called in wrong state. :contentReference[oaicite:5]{index=5}
    const isOpen = () => {
      try { return pop.matches(":popover-open"); } catch { return false; }
    };

    const positionPopover = () => {
		const r = anchor.getBoundingClientRect();

		// Reset any UA inset-based positioning that can fight your fixed coords.
		pop.style.inset = "auto";
		pop.style.right = "";
		pop.style.bottom = "";
		pop.style.margin = "0";
		pop.style.position = "fixed";

		// Measure after the popover is open (offsetWidth/Height are fine too)
		const pw = pop.offsetWidth;
		const ph = pop.offsetHeight;

		// 1) Put it just below the anchor
		let top = r.bottom + GAP_PX;

		// 2) Center-align popover to anchor
		let left = r.left + (r.width / 2) - (pw / 2);

		// 3) Clamp inside viewport so it never goes off-screen
		const minLeft = GAP_PX;
		const maxLeft = window.innerWidth - pw - GAP_PX;
		left = Math.max(minLeft, Math.min(left, maxLeft));

		// 4) If bottom overflow, flip above (still centered)
		if (top + ph + GAP_PX > window.innerHeight) {
			top = r.top - ph - GAP_PX;
		}
		top = Math.max(GAP_PX, top);

		pop.style.top = `${top}px`;
		pop.style.left = `${left}px`;
	};

    const open = () => {
      if (hideTimer) {
        clearTimeout(hideTimer);
        hideTimer = null;
      }

      if (!isOpen()) {
        pop.showPopover(); // Adds to top layer :contentReference[oaicite:6]{index=6}
      }

      // Wait a frame so layout is measurable, then place it
      requestAnimationFrame(positionPopover);
    };

    const scheduleClose = () => {
      if (hideTimer) clearTimeout(hideTimer);
      hideTimer = setTimeout(() => {
        if (isOpen()) pop.hidePopover(); // Removes from top layer :contentReference[oaicite:7]{index=7}
      }, HIDE_DELAY_MS);
    };

    // Pointer hover behavior
    anchor.addEventListener("pointerenter", open);
    anchor.addEventListener("pointerleave", scheduleClose);
    pop.addEventListener("pointerenter", open);
    pop.addEventListener("pointerleave", scheduleClose);

    // Keyboard: show on focus, hide on blur
    anchor.addEventListener("focus", open);
    anchor.addEventListener("blur", scheduleClose);

    // Keep position correct on scroll/resize while open
    window.addEventListener("scroll", () => { if (isOpen()) positionPopover(); }, true);
    window.addEventListener("resize", () => { if (isOpen()) positionPopover(); });
  });
})();


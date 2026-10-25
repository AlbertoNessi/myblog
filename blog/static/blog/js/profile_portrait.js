{
	const portrait = document.querySelector('.profile-portrait #profile-pic');
	const animationAllowed = window.matchMedia('(max-width: 900px) and (prefers-reduced-motion: no-preference)');
	let touchStartY = null;
	let touchStartScrollY = 0;
	let pullScale = 1;
	let animationFrame = null;
	let reboundAnimation = null;
	let nativeBounceActive = false;

	// Use finger movement because Safari can hold scrollY at 0 during refresh.
	function updatePortraitScale() {
		animationFrame = null;
		portrait.style.setProperty('--portrait-pull-scale', String(pullScale));
	}

	// Clear pending work before a new gesture or a return animation.
	function resetPortrait() {
		touchStartY = null;
		pullScale = 1;
		nativeBounceActive = false;
		if (animationFrame !== null) {
			window.cancelAnimationFrame(animationFrame);
			animationFrame = null;
		}
		if (reboundAnimation !== null) {
			reboundAnimation.cancel();
			reboundAnimation = null;
		}
		portrait.style.removeProperty('--portrait-pull-scale');
	}

	// Keep short pulls visible even when release occurs before the next frame.
	function bouncePortrait(distance) {
		const currentTransform = window.getComputedStyle(portrait).transform;
		const peakScale = 1 + Math.min(Math.max(distance / 400, 0.04), 0.15);
		resetPortrait();
		reboundAnimation = portrait.animate([
			{transform: currentTransform, offset: 0, easing: 'ease-out'},
			{transform: 'scale(' + peakScale + ')', offset: 0.22, easing: 'ease-in-out'},
			{transform: 'scale(0.985)', offset: 0.7, easing: 'ease-out'},
			{transform: 'scale(1)', offset: 1}
		], {duration: 340});
	}

	function startPortraitPull(event) {
		resetPortrait();
		if (!animationAllowed.matches || event.touches.length !== 1) {
			return;
		}
		touchStartY = event.touches[0].clientY;
		touchStartScrollY = Math.max(0, window.scrollY);
	}

	function movePortraitPull(event) {
		if (touchStartY === null) {
			return;
		}
		if (!animationAllowed.matches || event.touches.length !== 1) {
			resetPortrait();
			return;
		}

		let scale = 1;
		if (window.scrollY <= 0) {
			// Exclude the part of the gesture used to reach the page top.
			const distance = Math.max(0, event.touches[0].clientY - touchStartY - touchStartScrollY);
			scale = 1 + Math.min(distance / 400, 0.15);
		}
		// Normal scrolling and pulls at the size limit need no new frame.
		if (scale === pullScale) {
			return;
		}
		pullScale = scale;
		if (animationFrame === null) {
			animationFrame = window.requestAnimationFrame(updatePortraitScale);
		}
	}

	function endPortraitPull(event) {
		if (touchStartY === null) {
			return;
		}

		let distance = 0;
		if (animationAllowed.matches && window.scrollY <= 0 && event.changedTouches.length === 1) {
			// The final touch position is available even without a painted move.
			distance = Math.max(0, event.changedTouches[0].clientY - touchStartY - touchStartScrollY);
		}
		if (distance >= 8) {
			bouncePortrait(distance);
			return;
		}
		resetPortrait();
	}

	// Momentum can reach the top after the finger has left the screen.
	function followNativeBounce() {
		if (window.scrollY >= 0) {
			nativeBounceActive = false;
			return;
		}
		if (!animationAllowed.matches || touchStartY !== null || nativeBounceActive) {
			return;
		}
		if (reboundAnimation === null || reboundAnimation.playState !== 'running') {
			bouncePortrait(-window.scrollY);
		}
		nativeBounceActive = true;
	}

	window.addEventListener('touchstart', startPortraitPull, {passive: true});
	window.addEventListener('touchmove', movePortraitPull, {passive: true});
	window.addEventListener('touchend', endPortraitPull, {passive: true});
	window.addEventListener('touchcancel', resetPortrait, {passive: true});
	window.addEventListener('scroll', followNativeBounce, {passive: true});
	window.addEventListener('pageshow', resetPortrait);
	animationAllowed.addEventListener('change', resetPortrait);
}

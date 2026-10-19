{
	const menu = document.querySelector('.section-menu');
	const toggle = document.querySelector('#menu-toggle');
	const navigation = document.querySelector('#section-navigation');
	const mobileLayout = window.matchMedia('(max-width: 900px)');

	// Set the mobile menu state. Keep the desktop links visible.
	function updateNavigation(isOpen) {
		const isMobile = mobileLayout.matches;
		toggle.hidden = !isMobile;
		toggle.setAttribute('aria-expanded', String(isMobile && isOpen));
		navigation.hidden = isMobile && !isOpen;
	}

	toggle.addEventListener('click', () => {
		updateNavigation(toggle.getAttribute('aria-expanded') === 'false');
	});

	navigation.addEventListener('click', (event) => {
		if (event.target.closest('a')) {
			updateNavigation(false);
		}
	});

	document.addEventListener('click', (event) => {
		if (!navigation.contains(event.target) && !toggle.contains(event.target)) {
			updateNavigation(false);
		}
	});

	document.addEventListener('keydown', (event) => {
		if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
			updateNavigation(false);
			toggle.focus();
		}
	});

	mobileLayout.addEventListener('change', () => {
		updateNavigation(false);
	});

	menu.classList.add('has-menu');
	updateNavigation(false);
}

{
	const form = document.querySelector('.quotes-search');
	const input = form.querySelector('input');
	const clear = form.querySelector('a');
	const list = document.querySelector('.quotes-list');
	const errorMessage = document.querySelector('#quotes-search-error');
	let timer;
	let controller;
	let composing = false;

	async function searchQuotes() {
		const request = new AbortController();
		controller = request;
		const url = new URL(form.action);
		url.searchParams.set('q', input.value.trim());
		errorMessage.hidden = true;
		list.setAttribute('aria-busy', 'true');

		try {
			const response = await fetch(url, {signal: request.signal});
			if (!response.ok) {
				throw new Error('Quote search failed.');
			}
			const page = new DOMParser().parseFromString(await response.text(), 'text/html');
			// An old response must not replace results for the current input.
			if (request.signal.aborted) {
				return;
			}
			list.replaceChildren(...page.querySelector('.quotes-list').childNodes);
			history.replaceState(null, '', url);
		} catch (error) {
			if (error.name !== 'AbortError') {
				errorMessage.hidden = false;
				throw error;
			}
		} finally {
			if (controller === request) {
				list.removeAttribute('aria-busy');
			}
		}
	}

	function scheduleSearch(event) {
		if (event.type === 'compositionstart') {
			composing = true;
		} else if (event.type === 'compositionend') {
			composing = false;
		}
		clearTimeout(timer);
		if (controller) {
			controller.abort();
		}
		clear.toggleAttribute('data-empty', !input.value.trim());
		// Wait for the keyboard to commit text before a search request.
		if (composing || event.isComposing) {
			return;
		}
		timer = setTimeout(searchQuotes, 250);
	}

	input.addEventListener('input', scheduleSearch);
	input.addEventListener('compositionstart', scheduleSearch);
	input.addEventListener('compositionend', scheduleSearch);

	clear.addEventListener('click', (event) => {
		if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
			return;
		}
		event.preventDefault();
		input.value = '';
		composing = false;
		input.focus({preventScroll: true});
		input.dispatchEvent(new Event('input', {bubbles: true}));
	});
}

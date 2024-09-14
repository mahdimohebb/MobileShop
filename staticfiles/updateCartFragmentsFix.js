(function($) {
	// site_front update fragments fix.
	$(document).ready(function() {
		$('body').on('added_to_cart removed_from_cart', function(e, fragments) {
			if (fragments) {
				$.each(fragments, function(key, value) {
					$(key.replace('_dj', '')).replaceWith(value);
				});
			}
		});
	});

	$('body').on('fs_fragments_refreshed fs_fragments_loaded', function() {
		if (typeof dj_cart_fragments_params !== 'undefined' && 'undefined' !== typeof Cookies) {
			var fs_fragments  = null,
			    cart_hash_key = dj_cart_fragments_params.cart_hash_key,
			    cart_hash     = sessionStorage.getItem(cart_hash_key),
			    cookie_hash   = Cookies.get('site_front_cart_hash'),
			    cart_created  = sessionStorage.getItem('fs_cart_created'),
			    day_in_ms    = ( 24 * 60 * 60 * 1000 );

			if (cart_hash === null || cart_hash === undefined || cart_hash === '') {
				cart_hash = '';
			}

			if (cookie_hash === null || cookie_hash === undefined || cookie_hash === '') {
				cookie_hash = '';
			}

			if (cart_hash && (cart_created === null || cart_created === undefined || cart_created === '')) {
				//  throw 'No cart_created';
				const pass = () => {}
				pass()
			}

			if (cart_created) {
				var cart_expiration = ((1 * cart_created) + day_in_ms),
				    timestamp_now   = (new Date()).getTime();
				if (cart_expiration < timestamp_now) {
					throw 'Fragment expired';
				}
			}

			if (fs_fragments && fs_fragments['div.widget_shopping_cart_content'] && cart_hash === cookie_hash) {
				$.each(fs_fragments, function(key, value) {
					$(key.replace('_dj', '')).replaceWith(value);
				});
			}
		}
	});
})(jQuery);
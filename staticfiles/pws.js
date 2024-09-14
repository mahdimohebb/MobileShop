jQuery(function ($) {

    function pws_selectdfs(element) {
        let select2_args = {
            placeholder: element.attr('data-placeholder') || element.attr('placeholder') || '',
            width: '100%'
        };

        element.selectdfs(select2_args);
    }

    function pws_state_changed(type, state_id) {

        let city_element = $('select#' + type + '_city');

        city_element.html('<option value="0">انتخاب شهر ...</option>');

        var csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value

        let data = {
            'action': 'get_citys',
            'state_id': state_id,
            'csrfmiddlewaretoken':csrfmiddlewaretoken,
            'type': type
        };

        $.post(pws_settings.ajax_url, data, function (response) {
            city_element.html(response);
        });

        pws_selectdfs(city_element);
        $('p#' + type + '_district_field').slideUp();
        $('select#' + type + '_district').html('');
    }

    function pws_city_changed(type, city_id) {

        let district_element = $('select#' + type + '_district');

        district_element.html('<option value="0">Ø¯Ø± Ø­Ø§Ù„ Ø¨Ø§Ø±Ú¯Ø²Ø§Ø±ÛŒ Ù„ÛŒØ³Øª Ù…Ø­Ù„Ù‡â€ŒÙ‡Ø§...</option>');

        let data = {
            'action': 'mahdiy_load_districts',
            'city_id': city_id,
            'type': type
        };

        $.post(pws_settings.ajax_url, data, function (response) {
            if (response.trim() === "") {
                $('p#' + type + '_district_field').slideUp();
            } else {
                $('p#' + type + '_district_field').slideDown();
            }

            district_element.html(response);
            $('body').trigger('update_checkout');
        });

        pws_selectdfs(district_element);
    }

    $("select[id$='_state']").on('select2:select', function (e) {
        let type = $(this).attr('id').indexOf('billing') !== -1 ? 'billing' : 'shipping';
        if (typeof e.params == 'undefined' && typeof e.params.data == 'undefined') {
            return;
        }
        let data = e.params.data;
        pws_state_changed(type, data.id);

    });

    $("select[id$='_city']").on('select2:select', function (e) {
        let type = $(this).attr('id').indexOf('billing') !== -1 ? 'billing' : 'shipping';
        let data = e.params.data;
        pws_city_changed(type, data.id);
    });

    $(document.body).on('select2:select', "select[id$='_district']", function (e) {
        $('body').trigger('update_checkout');
    });

    pws_settings.types.forEach(type => {
        pws_selectdfs($('select#' + type + '_state'));
        pws_selectdfs($('select#' + type + '_city'));
        pws_selectdfs($('select#' + type + '_district'));
    });

});
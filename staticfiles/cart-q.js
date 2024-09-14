	
var total_price = document.querySelector('.Total-price')
var price = total_price.getAttribute('data-price');
price = convertToPersianNumber(price)
total_price.innerHTML = price

function qty_change(action_, id_, e_price){
    var qtn_input = document.querySelector('#quantity_'+id_);
    var qtn_v = qtn_input.value;
    var count = qtn_v;
    var t_price = document.querySelector('.amount-'+id_+' > bdi')	
    document.querySelector('#post-8 > div > div > div > form > div > table > tbody > tr.dj-cart-action-row > td > div > button').disabled = false;

    if (action_ == 'plus'){
        qtn_input.value = parseInt(qtn_v) + 1;
        count = parseInt(count) + 1;
    }else if (action_ == 'minus'){
        if (qtn_v != 0){
            qtn_input.value = parseInt(qtn_v) - 1;
            count = parseInt(count) - 1;
        }
    }
    
    t_price.innerHTML = '<bdi data-price="'+ parseInt(e_price)*parseInt(count) + '">'+ parseInt(e_price)*parseInt(count)  +'&nbsp;<span class="site_front-Price-currencySymbol">تومان</span></bdi>'
    FormatPrices('bdi[data-price="' + parseInt(e_price)*parseInt(count)  +  '"]');
}
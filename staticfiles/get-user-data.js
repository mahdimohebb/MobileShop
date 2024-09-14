var url = '/site-ajax';

var wishlist_count = 0;

var xhr = new XMLHttpRequest();

xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200){
        var response = JSON.parse(xhr.responseText);
        console.log(response)
    }
};

var form_data = new FormData();

form_data.append('action', 'Get_data')
form_data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value)


xhr.open("POST", url, true)
xhr.setRequestHeader('Content-Type', 'application/json')


xhr.send(form_data)
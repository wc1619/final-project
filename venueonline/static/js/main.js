// var user = '{{ request.user }}'

function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getToken('csrftoken')

function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");

    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");

        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name === cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }

    // Return null if not found
    return null;
}
var cart = JSON.parse(getCookie('cart'))
var resInfo = JSON.parse(getCookie('ResInfo'))

if (cart == undefined){
    cart = {}
    console.log('Cart created!', cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

if (resInfo == undefined){
    resInfo = {}
    console.log('ResInfo created!', resInfo)
    document.cookie ='ResInfo=' + JSON.stringify(resInfo) + ";domain=;path=/"
}
else{
    console.log('ResInfo existed!', resInfo)
    document.cookie ='ResInfo=' + JSON.stringify(resInfo) + ";domain=;path=/"
}

// console.log('Cart:', cart)




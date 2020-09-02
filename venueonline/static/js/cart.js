var updateBtns = document.getElementsByClassName('update_cart')

for (i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function () {
        var foodId = this.dataset.foodid
        var action = this.dataset.action
        console.log("foodid:",foodId,"action:",action)
        console.log('user:',user)

        if(user==='AnonymousUser'){
            addGuestItem(foodId,action)
        }else{
            updateUserOrder(foodId,action)
        }

    })
}


function addGuestItem(foodId,action){
    console.log('Not logged in.........')

    if(action == 'add'){
        if(cart[foodId] == undefined){
            cart[foodId] = {'quantity':1}
        }else{
            cart[foodId]['quantity'] += 1
        }
        location.reload() //No idea whether the page is not refreshed..
    }
    console.log('Cart')
    if(action == 'remove'){
        cart[foodId]['quantity'] -= 1

        if(cart[foodId]['quantity'] <= 0){
            console.log('Delete the Item...')
            delete cart[foodId]
        }
        location.reload()
    }
    console.log('Cart',cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}


function updateUserOrder(foodId,action) {
    console.log('User is authenticated, sending data...')

    var url = '/fasteat/update_item/'

    fetch(url,{
        method:"POST",
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'foodId':foodId,'action':action})
    })

    .then((response)=>{
        return response.json();
    })

    .then( data =>{
        location.reload();
        console.log('data',data)
    })
}



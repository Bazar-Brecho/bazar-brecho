var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var product_id = this.dataset.product
        var action = this.dataset.action
        console.log('product_id:', product_id, 'action:', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            addCookieItem(product_id, action)
        }
    })
}

function addCookieItem(product_id,action){
    console.log('User is not authenticated')

    if (action == 'add'){
        if(cart[product_id] == undefined){
            cart[product_id] = {'quantity':1}
        }else{
            cart[product_id]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[product_id]['quantity'] -= 1

        if(cart[product_id]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[product_id]
        }
    } 
    console.log('Cart:', cart)
    document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/"
    location.reload()   

}

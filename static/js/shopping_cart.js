const updateBtn = document.getElementsByClassName('update-cart')
const URL = 'http://localhost:8000/store/'

getBtnValues(updateBtn)


function getBtnValues(btn) {
    for (let index = 0; index < btn.length; index++) {
        btn[index].addEventListener('click', function(){
            const product = this.dataset.product
            const action = this.dataset.action
            console.log('product id: ', product, 'action: ', action)
            updateUserOrder(product, action)
        })
    }    
}


function updateUserOrder(product_id, action){
    let url = URL + 'update-cart/'
    console.log('Sending data...')

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'product_id': product_id,
            'action': action,
        })
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        location.reload()
    })
}



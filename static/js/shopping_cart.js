let updateBtn = document.getElementById('update-cart')

updateBtn.addEventListener('click', function(){
    const product = this.dataset.product
    const action  = this.dataset.action

    console.log('product: ', product, 'action: ', action)
    console.log('user: ', user)
    updateUserOrder(product, action)
})

// function updateUserOrder(product, action) {
//     let url = '/update_cart/'

//     fetch(url, {
//         method: 'POST',
//         headers: {
//             content
//         }
//     })
// }
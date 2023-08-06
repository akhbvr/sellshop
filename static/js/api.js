function deleteProduct(id, i_d) {
    console.log(id);
    const url = `http://localhost:8000/api/wishlist/${id}/${i_d}/`;

    fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => {
            if (response.ok) {
                alert('Product removed from wishlist successfully');
                window.location.reload();
            } else {
                alert('Error removing product from wishlist', response.data);
            }
        })
        .catch(error => {
            alert('Error removing product from wishlist:', error.data);
        });
}

function addProduct(id) {
    const formData = {
        "product_variation": [id],
    };

    fetch("http://localhost:8000/api/wishlist/", {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                // "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg4OTA0NDQ1LCJpYXQiOjE2ODg5MDA4NDUsImp0aSI6ImM1OWNjY2MyZDM0MTQwNzVhMjNhMTljNzMzNTQ4YmI1IiwidXNlcl9pZCI6N30.fpripW9EWt69yytNwIaIZSs8StkYRSG1w1R4rcmGD8U",
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                alert('Product added successfully');
                window.location.reload();
            } else {
                alert('The product is in the wishlist or an error occurred while adding the product');
            }
        })
        .catch(error => {
            alert('The product is in the wishlist or an error occurred while adding the product:', error);
        });
}

function addBasket(product_id) {
    const formData = {
        "product_variation": product_id
    }
    fetch("http://127.0.0.1:8000/api/basket/", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5NTc5MDAyLCJpYXQiOjE2ODk1NzU0MDIsImp0aSI6IjM2ODMxOTVkNzdmOTQ1ZWRiYzlhMzIxMTkzZDA5OGJmIiwidXNlcl9pZCI6N30.6EWUb31BOkCJu0Hx4HMUfnyxXMydBnCZqLbArnP4Uk8",
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if(response.ok){
            alert("Product added successfully")
            window.location.reload()
        } else {
            alert("The product is in the basket or an error occurred while adding the product:", response.data);
        }
    })
    .catch(error => {
        alert("The product is in the basket or an error occurred while adding the product:", error.data)
    })
}

function deleteBasket(product_id) {
    fetch(`http://127.0.0.1:8000/api/basket/${product_id}/`, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5NTc5MDAyLCJpYXQiOjE2ODk1NzU0MDIsImp0aSI6IjM2ODMxOTVkNzdmOTQ1ZWRiYzlhMzIxMTkzZDA5OGJmIiwidXNlcl9pZCI6N30.6EWUb31BOkCJu0Hx4HMUfnyxXMydBnCZqLbArnP4Uk8"
        }
    })
    .then(response => {
        if(response.ok) {
            alert("Product removed from basket successfully.")
            window.location.reload()
        } else {
            alert("Error removing product from basket:", response.data)
        }
    })
    .catch(error => {
        alert("Error removing product from basket:", error.data)
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", async function(event){
    let res = await fetch("http://127.0.0.1:8000/api/basket/", {
        method: "GET",
        headers: {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5NTc5MDAyLCJpYXQiOjE2ODk1NzU0MDIsImp0aSI6IjM2ODMxOTVkNzdmOTQ1ZWRiYzlhMzIxMTkzZDA5OGJmIiwidXNlcl9pZCI6N30.6EWUb31BOkCJu0Hx4HMUfnyxXMydBnCZqLbArnP4Uk8"
        }
    })
    let products = await res.json()
    let basket_section = document.getElementById("cartdrop")
    let totalProduct = document.getElementById("total_product")
    totalProduct.innerHTML = products[0].product_variation.length

    console.log(products[0].product_variation.length)

    for(let product of products[0].product_variation){
        basket_section.innerHTML +=`
        <div class="sin-itme clearfix">

            <i class="mdi mdi-close" onclick="deleteBasket(${product.product_variation.id})"></i>
            <a class="cart-img" href="cart.html"><img src="${product.product_variation.main_image}" alt="" /></a>

            <div class="menu-cart-text">

                <a href="#"><h5>${product.product_variation.product.name}</h5></a>
                ${product.product_variation.product_attribute_values.map(attribute => `<span>${attribute.attribute.name}: ${attribute.value}</span>`).join('')}
                <input type="number" hidden value="${product.product_variation.price}" class="price">
                <strong>$${product.product_variation.price}</strong>

            </div>

        </div>
        <hr>
        `
    }
    let prices = document.querySelectorAll(".price")
    let totalAmountView = document.getElementById("totat_amount_view")
    let sum_price = 0
    prices.forEach(element => {
        sum_price += parseInt(element.value)
    });
    totalAmountView.innerHTML = sum_price
    basket_section.innerHTML += `
    <div class="total">
        <span>total <strong>= $${sum_price}</strong></span>
    </div>
    `

})
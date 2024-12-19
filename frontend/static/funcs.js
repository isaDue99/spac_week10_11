
// profile.html

function changeUser(elm) {
    localStorage.setItem("profile", elm.value);

    location.reload();
}

function loadProfile() {
    if (localStorage.getItem("profile")) {
        let profile = JSON.parse(localStorage.getItem('profile'));
        let option = document.getElementById("option-" + profile.CustomerID);
        option.setAttribute("selected", "");

        let idSpan = document.getElementById("customer-id");
        idSpan.innerText = profile.CustomerID;

        let firstSpan = document.getElementById("customer-first");
        firstSpan.innerText = profile.FirstName;

        let lastSpan = document.getElementById("customer-last");
        lastSpan.innerText = profile.LastName;
    }
}


// index.html and product.html

function add1ToCart(elm) {        
    let obj = JSON.parse(elm.value);

    // get cart if it exists
    let cart = [];
    if (localStorage.getItem('cart')) {
        cart = JSON.parse(localStorage.getItem('cart'));
    }

    // check if id is already in cart
    let obj_i = cart.findIndex((element) => obj.ProductID == element.ProductID);
    if (obj_i == -1) {
        // not in cart, add it to cart and set quantity to 1        
        cart.push({'ProductID': obj.ProductID, 'Name': obj.Name, 'Quantity': 1});
    } else {
        // it is in cart, increase quantity by 1        
        cart[obj_i].Quantity = cart[obj_i].Quantity + 1;
    }

    // save to storage
    localStorage.setItem("cart", JSON.stringify(cart));

    location.reload();
}


// cart.html

function confirmCart() {
    // somehow send localstorage data to backend...
    let CustomerID = 1;
    if (localStorage.getItem("profile")) {
        let profile = JSON.parse(localStorage.getItem('profile'));
        CustomerID = profile.CustomerID;
    }

    let IDsQts = [];
    if (localStorage.getItem("cart")) {
        let cart = JSON.parse(localStorage.getItem('cart'));
        for (let i = 0; i < cart.length; i++) {
            let elm = cart[i];
            IDsQts.push(
                {"ProductID": elm.ProductID, "Quantity": elm.Quantity}
            );
        }
    } else {
        // dont send anything if cart is empty!
        return
    }

    // send the data to frontend routes
    fetch("http://127.0.0.1:3000/cart",
        {
            method: "POST",
            body: JSON.stringify
            ({
              CustomerID: CustomerID,
              Cart: IDsQts
            }),
            headers: {
              "Content-type": "application/json",
            },
          });

    // reset cart
    resetCart();

    location.href = "http://127.0.0.1:3000";
}

function remove1FromCart(id) {
    let cart = [];

    // get cart
    cart = JSON.parse(localStorage.getItem('cart'));

    // get the product in the cart
    let obj_i = cart.findIndex((element) => id.value == element.ProductID);

    // either decrement it's quantity or remove it entirely
    if ((cart[obj_i].Quantity - 1) == 0) {
        cart.splice(obj_i, 1);
    } else {
        cart[obj_i].Quantity = cart[obj_i].Quantity - 1;
    }

    // save to storage
    localStorage.setItem("cart", JSON.stringify(cart));

    if (cart.length == 0) {
        // if whole cart is empty then reset
        resetCart();
    }

    location.reload();
}

function removeProductFromCart(id) {
    let cart = [];

    // get cart
    cart = JSON.parse(localStorage.getItem('cart'));

    // get the product in the cart
    let obj_i = cart.findIndex((element) => id.value == element.ProductID);

    // remove the product
    cart.splice(obj_i, 1);

    // save to storage
    localStorage.setItem("cart", JSON.stringify(cart));

    if (cart.length == 0) {
        // if whole cart is empty then reset
        resetCart();
    }

    location.reload();
}

function resetCart() {
    localStorage.removeItem("cart");

    location.reload();
}

function constructCart() {
    let data = [];
    let ul = document.getElementById("cart-items");
    if (localStorage.getItem("cart")) {
        data = JSON.parse(localStorage.getItem('cart'));
        // if cart is already constructed, empty it
        ul.innerHTML = "";
    }

    // construct it
    for (let i = 0; i < data.length; i++) {
        let elm = data[i];

        //// create the bits that go into a list item
        let html = "<span class=\"product-name\">" 
        + elm.Name
        + "</span> <span class=\"product-id\">(No."
        + elm.ProductID
        + ")</span> <span class=\"product-quantity\">Qt: "
        + elm.Quantity
        + "</span> ";

        // buttons
        let add_btn = document.createElement('button');
        add_btn.setAttribute("onclick", "add1ToCart(this)");
        add_btn.setAttribute("value", '{"ProductID": "' + elm.ProductID + '", "Name": "' + elm.Name + '"}');
        add_btn.textContent = "+";

        let dec_btn = document.createElement('button');
        dec_btn.setAttribute("onclick", "remove1FromCart(this)");
        dec_btn.setAttribute("value", elm.ProductID);
        dec_btn.textContent = "-";

        let rem_btn = document.createElement('button');
        rem_btn.setAttribute("onclick", "removeProductFromCart(this)");
        rem_btn.setAttribute("value", elm.ProductID);
        rem_btn.textContent = "X";

        // add the buttons into a separate element
        let btns = document.createElement('span');
        btns.setAttribute("class", "product-btns");
        btns.appendChild(add_btn);
        btns.appendChild(dec_btn);
        btns.appendChild(rem_btn);

        // finally construct list item
        let li = document.createElement('li');
        li.setAttribute("class", "cart-item");
        li.innerHTML = html;
        li.appendChild(btns);

        ul.appendChild(li);
    }
}

function loadCart() {
    if (localStorage.getItem("cart") && JSON.parse(localStorage.getItem("cart")).length != 0) {
        constructCart();
    }

    if (localStorage.getItem("profile")) {
        let profile = JSON.parse(localStorage.getItem('profile'));
        let title = document.getElementById("cart-title");
        title.innerText = title.innerText + ", " + profile.FirstName + " " + profile.LastName;
    }
}
  
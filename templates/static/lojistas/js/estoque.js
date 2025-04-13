document.addEventListener('DOMContentLoaded', function () {
    const cartButton = document.querySelector('.cart-button');
    const cartDrawerOverlay = document.querySelector('.cart-drawer__overlay');
    const cartDrawerCloseButton = document.querySelector('.cart-drawer__header .btn-close');

    cartButton.addEventListener('click', () => {
        cartDrawerOverlay.classList.add('open');
    });

    cartDrawerCloseButton.addEventListener('click', () => {
        cartDrawerOverlay.classList.remove('open');
    });

    cartDrawerOverlay.addEventListener('click', (event) => {
        if (event.target === cartDrawerOverlay) {
            cartDrawerOverlay.classList.remove('open');
        }
    });

    const catalogGrid = document.querySelector('.catalog-grid');
    const products = [
        // Example products
        { title: 'Produto 01', price: 'R$ 9,99', image: 'https://via.placeholder.com/300/f5f5f5/999999/?text=Produto+01' },
        { title: 'Produto 02', price: 'R$ 19,99', image: 'https://via.placeholder.com/300/f5f5f5/999999/?text=Produto+02' },
        // Add more products as needed
    ];

    products.forEach(product => {
        const colDiv = document.createElement('div');
        colDiv.className = 'col';
        const productCard = document.createElement('div');
        productCard.className = 'product-card card h-100';
        productCard.innerHTML = `
            <img src="${product.image}" class="product-card__img img-fluid" alt="${product.title}">
            <div class="card-body">
                <h5 class="product-card__title card-title">${product.title}</h5>
                <p class="product-card__price card-text">${product.price}</p>
                <button class="btn btn-primary w-100" data-bs-toggle="modal" data-bs-target="#quick-add-to-cart">Adicionar</button>
            </div>
        `;
        colDiv.appendChild(productCard);
        catalogGrid.appendChild(colDiv);
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const addToBagButtons = document.querySelectorAll('.add-to-bag');
    const bagItemsList = document.getElementById('bag-items');

    addToBagButtons.forEach(button => {
        button.addEventListener('click', addToBag);
    });

    function addToBag(event) {
        const product = event.target.closest('.product');
        const productName = product.querySelector('h3').innerText;
        const productImageSrc = product.querySelector('img').src;

        const bagItem = document.createElement('li');
        bagItem.classList.add('bag-item');

        bagItem.innerHTML = `
            <img src="${productImageSrc}" alt="${productName}">
            <span>${productName}</span>
        `;

        bagItemsList.appendChild(bagItem);
    }
});

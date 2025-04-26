document.addEventListener('DOMContentLoaded', function () {
    const items = [
        {
            image: 'images/_wilbur.jpg',
            name: 'Item 1',
            description: 'Name: Wilbur Jr,<br>Sire: Wilbur Senior,<br>Mother: Bessie,<br>Age: 5 years,<br>Breed: Angus,<br>Price: $2500.00'
        },
        {
            image: 'images/_wilbur.jpg',
            name: 'Item 2',
            description: 'Name: Wilbur Senior,<br>Sire: Wilbur The Great,<br>Mother: Jessie,<br>Age: 7 years,<br>Breed: Angus,<br>Price: $5500.00'
        }
    ];

    const itemContainer = document.getElementById('item-container');

    items.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('item');

        const img = document.createElement('img');
        img.src = item.image;
        img.alt = item.name;

        const infoDiv = document.createElement('div');
        infoDiv.classList.add('info');

        const itemName = document.createElement('h3');
        itemName.textContent = item.name;

        const itemDescription = document.createElement('p');
        itemDescription.innerHTML = item.description; // Use innerHTML to support <br> tags

        infoDiv.appendChild(itemName);
        infoDiv.appendChild(itemDescription);

        itemDiv.appendChild(img);
        itemDiv.appendChild(infoDiv);

        itemContainer.appendChild(itemDiv);
    });
});

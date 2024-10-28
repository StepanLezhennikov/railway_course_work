// Открытие/закрытие карточки вагона при клике
function toggleDetails(card) {
    const details = card.querySelector('.wagon-details');
    const isDisplayed = details.style.display === 'block';
    details.style.display = isDisplayed ? 'none' : 'block';
}

// Логика выбора места
function selectSeat(event, seatElement, isOccupied) {
    event.stopPropagation(); // Останавливаем всплытие события, чтобы карточка не закрывалась

    // Проверяем, занято ли место
    if (isOccupied) {
        alert('Это место уже занято');
        return;
    }

    // Переключение состояния места (выбранное или нет)
    if (seatElement.classList.contains('selected')) {
        seatElement.classList.remove('selected');
        removeSeatFromSelection(seatElement.dataset.seatNumber, seatElement.dataset.wagonNumber);
    } else {
        seatElement.classList.add('selected');
        addSeatToSelection(seatElement.dataset.seatNumber, seatElement.dataset.wagonNumber);
    }
}

// Добавление выбранного места в список
function addSeatToSelection(seatNumber, wagonNumber) {
    const selectedSeatsList = document.getElementById('selected-seats-list');
    const listItem = document.createElement('li');
    listItem.textContent = `Вагон №${wagonNumber}, Место №${seatNumber}`;
    listItem.setAttribute('data-seat-number', seatNumber);
    listItem.setAttribute('data-wagon-number', wagonNumber);
    selectedSeatsList.appendChild(listItem);
}

// Удаление места из списка выбранных мест
function removeSeatFromSelection(seatNumber, wagonNumber) {
    const selectedSeatsList = document.getElementById('selected-seats-list');
    const listItem = selectedSeatsList.querySelector(`[data-seat-number="${seatNumber}"][data-wagon-number="${wagonNumber}"]`);
    if (listItem) {
        selectedSeatsList.removeChild(listItem);
    }
}

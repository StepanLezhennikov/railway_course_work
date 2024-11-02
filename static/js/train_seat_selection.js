// train_seat_selection.js

// Открытие/закрытие карточки вагона при клике
function toggleDetails(card) {
    const details = card.querySelector('.wagon-details');
    const isDisplayed = details.style.display === 'block';
    details.style.display = isDisplayed ? 'none' : 'block';
}

// Логика выбора места
function selectSeat(event, seatElement, isOccupied) {
    event.stopPropagation(); // Останавливаем всплытие события, чтобы карточка не закрывалась

    if (isOccupied) {
        alert('Это место уже занято');
        return;
    }

    if (seatElement.classList.contains('selected')) {
        seatElement.classList.remove('selected');
        removeSeatFromSelection(seatElement.dataset.seatNumber, seatElement.dataset.wagonNumber);
    } else {
        seatElement.classList.add('selected');
        addSeatToSelection(seatElement.dataset.seatNumber, seatElement.dataset.wagonNumber);
    }
}

// Добавление выбранного места в список и скрытое поле формы
function addSeatToSelection(seatNumber, wagonNumber) {
    const selectedSeatsList = document.getElementById('selected-seats-list');
    const listItem = document.createElement('li');
    listItem.textContent = `Вагон №${wagonNumber}, Место №${seatNumber}`;
    listItem.setAttribute('data-seat-number', seatNumber);
    listItem.setAttribute('data-wagon-number', wagonNumber);
    selectedSeatsList.appendChild(listItem);

    updateSelectedSeatsData();
}

// Удаление места из списка выбранных мест и скрытого поля формы
function removeSeatFromSelection(seatNumber, wagonNumber) {
    const selectedSeatsList = document.getElementById('selected-seats-list');
    const listItem = selectedSeatsList.querySelector(`[data-seat-number="${seatNumber}"][data-wagon-number="${wagonNumber}"]`);
    if (listItem) {
        selectedSeatsList.removeChild(listItem);
    }

    updateSelectedSeatsData();
}

// Заполнение скрытого поля формы с выбранными местами
function updateSelectedSeatsData() {
    const selectedSeatsList = document.getElementById('selected-seats-list').children;
    const selectedSeats = Array.from(selectedSeatsList).map(item => ({
        seat_number: item.getAttribute('data-seat-number'),
        wagon_number: item.getAttribute('data-wagon-number')
    }));
    document.getElementById('selected-seats-data').value = JSON.stringify(selectedSeats);
}

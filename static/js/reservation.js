document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.querySelector('#id_reservation_date');
    const timeSelect = document.querySelector('#id_reservation_time');
    const restaurantInput = document.querySelector('#id_restaurant');

    if (!dateInput || !timeSelect || !restaurantInput) return;

    dateInput.addEventListener('change', function() {
        const selectedDate = dateInput.value;
        const restaurantId = restaurantInput.value;
        if (!selectedDate || !restaurantId) return;

        fetch(`/restaurants/${restaurantId}/timeslots/?date=${selectedDate}`)
            .then(response => response.json())
            .then(data => {
                timeSelect.innerHTML = '';
                if (data.length === 0) {
                    const option = document.createElement('option');
                    option.value = '';
                    option.textContent = 'No available times';
                    timeSelect.appendChild(option);
                } else {
                    data.forEach(slot => {
                        const option = document.createElement('option');
                        option.value = slot.value;
                        option.textContent = slot.label;
                        timeSelect.appendChild(option);
                    });
                }
            });
    });
});
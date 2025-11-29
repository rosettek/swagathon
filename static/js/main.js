document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('[data-filter-field]');
    const activeFiltersContainer = document.getElementById('active-filters');
    const searchForm = document.querySelector('form[method="GET"]');

    // Объект для хранения активных фильтров
    let activeFilters = {};

    // Загружаем фильтры из URL при загрузке страницы
    loadFiltersFromURL();

    // Обработчик для кнопок добавления фильтров
    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            const field = this.getAttribute('data-filter-field');
            addFilter(field);
        });
    });

    function addFilter(field) {
        if (activeFilters[field]) {
            // Фильтр для этого поля уже существует, выходим
            return;
        }

        // Создаем элемент фильтра
        const filterElement = document.createElement('div');
        filterElement.className = 'input-group mb-2 filter-item';
        filterElement.setAttribute('data-field', field);

        const fieldLabel = getFilterLabel(field);

        filterElement.innerHTML = `
            <span class="input-group-text">${fieldLabel}</span>
            <input type="text" class="form-control filter-input" data-field="${field}" value="${activeFilters[field] || ''}" placeholder="Введите значение">
            <button class="btn btn-outline-danger btn-remove-filter" type="button">&times;</button>
        `;

        activeFiltersContainer.appendChild(filterElement);

        // Добавляем фильтр в объект
        activeFilters[field] = activeFilters[field] || '';

        // Обработчик для удаления фильтра
        const removeButton = filterElement.querySelector('.btn-remove-filter');
        removeButton.addEventListener('click', function () {
            delete activeFilters[field];
            filterElement.remove();
        });

        // Обработчик для изменения значения фильтра
        const filterInput = filterElement.querySelector('.filter-input');
        filterInput.addEventListener('input', function () {
            activeFilters[field] = this.value;
        });
    }

    function getFilterLabel(field) {
        const labels = {
            'name': 'Название',
            'model': 'Модель',
            'country': 'Страна происхождения',
            'manufacturer': 'Производитель',
            'category': 'Название категории'
        };
        return labels[field] || field;
    }

    function loadFiltersFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        
        // Проверяем общее поле поиска 'q'
        const generalQuery = urlParams.get('q');
        if (generalQuery) {
            document.querySelector('input[name="q"]').value = generalQuery;
        }
        
        // Проверяем параметры фильтров
        const filterFields = ['name', 'model', 'country', 'manufacturer', 'category'];
        filterFields.forEach(field => {
            const value = urlParams.get(field);
            if (value) {
                activeFilters[field] = value;
                addFilter(field); // Создаем UI элемент для фильтра
            }
        });
    }

    // Обновляем URL перед отправкой формы
    searchForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Предотвращаем стандартную отправку
        
        const formData = new FormData(searchForm);
        const params = new URLSearchParams();
        
        // Добавляем общее поле поиска 'q'
        const generalQuery = formData.get('q');
        if (generalQuery) {
            params.set('q', generalQuery);
        } else {
            params.delete('q'); // Удаляем, если пустое
        }
        
        // Добавляем активные фильтры
        Object.keys(activeFilters).forEach(field => {
            if (activeFilters[field]) {
                params.set(field, activeFilters[field]);
            }
        });
        
        // Формируем новый URL
        const newURL = window.location.pathname + '?' + params.toString();
        window.location.href = newURL; // Перенаправляем на новый URL
    });
});
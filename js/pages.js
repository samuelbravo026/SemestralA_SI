// Modal functionality
const modal = document.getElementById('userModal');
const addUserBtn = document.getElementById('addUserBtn');
const addProductBtn = document.getElementById('addProductBtn');
const closeModalBtns = document.querySelectorAll('.close-modal');

if (addUserBtn) {
    addUserBtn.addEventListener('click', () => {
        modal.classList.add('active');
    });
}

if (addProductBtn) {
    addProductBtn.addEventListener('click', () => {
        const productModal = document.getElementById('productModal');
        if (productModal) {
            productModal.classList.add('active');
        }
    });
}

closeModalBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        modal.classList.remove('active');
        const productModal = document.getElementById('productModal');
        if (productModal) {
            productModal.classList.remove('active');
        }
    });
});

// Cerrar modal al hacer click fuera
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('active');
    }
    const productModal = document.getElementById('productModal');
    if (e.target === productModal) {
        productModal.classList.remove('active');
    }
});

// Select all checkboxes
const selectAll = document.querySelector('.select-all');
if (selectAll) {
    selectAll.addEventListener('change', function() {
        const checkboxes = document.querySelectorAll('.data-table tbody input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });
}

// Delete confirmation
const deleteButtons = document.querySelectorAll('.btn-icon:has(.fa-trash)');
deleteButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
            // Implementar lógica de eliminación
            console.log('Elemento eliminado');
        }
    });
});

// Form validation
const forms = document.querySelectorAll('.form');
forms.forEach(form => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = 'var(--danger-color)';
            } else {
                input.style.borderColor = 'var(--border-color)';
            }
        });

        if (isValid) {
            // Aquí iría la lógica para enviar el formulario
            console.log('Formulario válido, enviando...');

            // Simular envío exitoso
            alert('¡Datos guardados exitosamente!');
            modal.classList.remove('active');
            const productModal = document.getElementById('productModal');
            if (productModal) {
                productModal.classList.remove('active');
            }
            form.reset();
        } else {
            alert('Por favor, completa todos los campos requeridos.');
        }
    });
});

// Search functionality
const searchInputs = document.querySelectorAll('.search-box input');
searchInputs.forEach(searchInput => {
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const tableRows = document.querySelectorAll('.data-table tbody tr');

        if (tableRows.length > 0) {
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }

        const productCards = document.querySelectorAll('.product-card');
        if (productCards.length > 0) {
            productCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    });
});

// Filter functionality
const filterSelects = document.querySelectorAll('.filter-select');
filterSelects.forEach(select => {
    select.addEventListener('change', function() {
        // Implementar lógica de filtrado
        console.log('Filtro aplicado:', this.value);
    });
});

// Pagination
const paginationButtons = document.querySelectorAll('.btn-pagination:not(.active)');
paginationButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        if (!this.disabled) {
            document.querySelector('.btn-pagination.active')?.classList.remove('active');
            this.classList.add('active');
            // Implementar lógica de paginación
            console.log('Página:', this.textContent);
        }
    });
});

// Image preview for product image upload
const imageInputs = document.querySelectorAll('input[type="file"]');
imageInputs.forEach(input => {
    input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const preview = document.getElementById('imagePreview');
                if (preview) {
                    preview.src = event.target.result;
                    preview.style.display = 'block';
                }
            };
            reader.readAsDataURL(file);
        }
    });
});

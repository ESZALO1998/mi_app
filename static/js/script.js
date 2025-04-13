
let contadorMenores = 1;
var botonAgregarMenor = document.getElementById('btn-agragar-menor');

function agregarMenor() {
    contadorMenores++;
    const divMenores = document.getElementById('menores');
    const nuevoMenor = document.createElement('div');
    nuevoMenor.className = 'menor mb-3';
    nuevoMenor.innerHTML = `
        <div class="form-group">
            <label>Nombre del menor:</label>
            <input type="text" class="form-control" name="nombre_nino_${contadorMenores}" required>
        </div>
        <div class="form-group">
            <label>Identificación (NUIP):</label>
            <input type="text" class="form-control" name="identificacion_nino_${contadorMenores}" required>
        </div>
        <button type="button" class="btn btn-outline-danger btn-sm removeMenor">Eliminar</button>
    `;
    divMenores.appendChild(nuevoMenor);
}

// Añadir evento para agregar menores
botonAgregarMenor.addEventListener('click', agregarMenor);

// Añadir evento para eliminar menores
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('removeMenor')) {
        const menorDiv = event.target.closest('.menor');
        if (document.querySelectorAll('.menor').length > 1) {
            menorDiv.remove();
            window.contadorMenores--;
        } 
    }
});

var formulario = document.getElementById("formulario");

// Funcion para limpiar el formulario despues de enviarlo
formulario.addEventListener('submit', () => {
    
    setTimeout(() => formulario.reset(), 100); // Espera a que se envíe antes de limpiar
});




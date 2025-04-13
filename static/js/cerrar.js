var botonCerrar = document.getElementById('btn-cerrar-ventana');

function cerrarVentana() {
    window.close();
}

botonCerrar.addEventListener('click', cerrarVentana);
const documentoField = document.getElementById('documento');
const passwordField = document.getElementById('password');
const formInicio = document.getElementById('formInicio');
const spanEvento = document.getElementById('spanEvento');

let validationState = undefined;
//Evento de escucha submit para formulario
formInicio.addEventListener('submit', (e)=>{
    e.preventDefault()

    validationState = validarFormulario();
    if (validationState != '0'){
        spanEvento.innerText = validationState;
    }
    else formInicio.submit();
});

const validarFormulario = () =>{
    if (documentoField.value.trim().length < 6) return "Documento muy corto.\nMínimo 6 carácteres";
    else if (passwordField.value.trim().length < 8) return "Contraseña muy corta\nMínimo 8 carácteres.";

    return '0';
}
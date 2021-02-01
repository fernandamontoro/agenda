window.onload=function () {
  render();
  hiddeVerificacion();
  hiddeSuccess();
  hiddeFailure();
};

function render() {
    window.recaptchaVerifier=new firebase.auth.RecaptchaVerifier('recaptcha-container');
    recaptchaVerifier.render();
}
function phoneAuth() {
    //get the number
    var number=document.getElementById('number').value;
    //phone number authentication function of firebase
    //it takes two parameter first one is number,,,second one is recaptcha
    firebase.auth().signInWithPhoneNumber(number,window.recaptchaVerifier).then(function (confirmationResult) {
        //s is in lowercase
        window.confirmationResult=confirmationResult;
        coderesult=confirmationResult;
        console.log(coderesult);
        alert("SMS Enviado");

      hiddeSendSMS();
      showVerificacion();

    }).catch(function (error) {
        alert(error.message);
    });
}
function codeverify() {
  hiddeVerificacion();
    var code=document.getElementById('verificationCode').value;
    coderesult.confirm(code).then(function (result) {
      showSuccess();
      

    }).catch(function (error) {
      alert(error.message);
      alert("Hubo un error al momento del registro. Redireccionando al registro");
      window.location = "/registro";
    });
}

/* Manejo de los componentes */
function hiddeVerificacion(){
  let form = document.getElementById("verification");
  form.style.display='none';
  let button = document.getElementById("btnCheckCode");
  button.disabled = true;
}

function showVerificacion(){
  let form = document.getElementById("verification");
  form.style.display='';
  let button = document.getElementById("btnCheckCode");
  button.disabled = false;
  let formUsuario = document.getElementById("usuario");
  formUsuario.style.display = "none";
  let formCorreo = document.getElementById("correo");
  formCorreo.style.display = "none"
  let formContrasena = document.getElementById("contrasena");
  formContrasena.style.display = "none";
  let formContrasena2 = document.getElementById("contrasena2");
  formContrasena2.style.display = "none";
}

function hiddeSendSMS(){
  let form = document.getElementById("sendSMS");
  form.style.display='none';
  let button = document.getElementById("btnSendSMS");
  button.disabled = true;
}

function showSendSMS(){
  let form = document.getElementById("sendSMS");
  form.style.display='';
  let button = document.getElementById("btnSendSMS");
  button.disabled = false;
}

function hiddeSuccess(){
  let form = document.getElementById("success");
  form.style.display='none';
}

function showSuccess(){
  let form = document.getElementById("success");
  form.style.display='';
}

function hiddeFailure(){
  let form = document.getElementById("failure");
  form.style.display='none';
}

function showFailure(){
  let form = document.getElementById("failure");
  form.style.display='';
}
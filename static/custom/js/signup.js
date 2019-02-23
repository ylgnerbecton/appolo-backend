// MASKS
$('.masked-date').inputmask('99/99/9999', { placeholder: '__/__/____' });
$('.masked-cpf').inputmask('999.999.999-99', { placeholder: '___.___.___-__' });
$(".masked-phone").inputmask({mask: ["(99) 9999-9999", "(99) 99999-9999"], keepStatic: true});

// CPF VALIDATOR
$('.masked-cpf').cpfcnpj({
    validate: 'cpf',
    handler: '.masked-cpf',
    ifValid: function (input) {
        $("#cpf_line").removeClass("focused error");
    },
    ifInvalid: function (input) { 
        $("#cpf_line").addClass("focused error");
        $(input).val(''); 
    }
});

// SUBMIT FORM
$('#signup-form').submit(function(event) {
    event.preventDefault();
    var html = "";
    var formData = new FormData();

    formData.append("full_name", $(id_full_name).val());
    formData.append("email", $(id_email).val());
    formData.append("cpf", String($(id_cpf).val()).replace(/\D/g,''));
    formData.append("phone", $(id_phone).val());
    formData.append("image", $(id_image).val());
    formData.append("birth_date", $(id_birth_date).val());
    formData.append("user_terms", $(id_user_terms).val());
    formData.append("password", $(id_password).val());
    formData.append("confirm_password", $(id_confirm_password).val());

    formData.append("csrfmiddlewaretoken", $("#signup-form input[name='csrfmiddlewaretoken']").val());

    $.ajax({
        url: '',
        type: 'POST',
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        beforeSend: function (response) {
            //$.LoadingOverlay("show");
        },
        success: function (response) {
            //$.LoadingOverlay("hide");
            alert("Cadastro realizado com sucesso!");
            window.location.href = response.redirect;
        },
        error: function(response) {
            //$.LoadingOverlay("hide");
            alert(response.responseJSON.message);
        }
    });
});
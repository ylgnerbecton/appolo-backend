$('.masked-cpf').inputmask('999.999.999-99', { placeholder: '___.___.___-__' });
$('.masked-cnpj').inputmask('99.999.999/9999-99', { placeholder: '__.___.___/____-__' });
$(".masked-zipcode").inputmask('99.999-999', { placeholder: '_.__-__' });
$(".masked-date").inputmask('99/99/9999', { placeholder: '__/__/____' });
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

// CPF VALIDATOR
$('.masked-cnpj').cpfcnpj({
    validate: 'cnpj',
    handler: '.masked-cnpj',
    ifValid: function (input) {
        $("#cnpj_line").removeClass("focused error");
    },
    ifInvalid: function (input) { 
        $("#cnpj_line").addClass("focused error");
        $(input).val(''); 
    }
});

$(zip_code_id).focusout(function(event){
    var cep = String($(this).val()).replace(/\D/g,'');
    $.ajax({
        url: url_cep_service,
        type: 'GET',
        data: {cep:cep},
        success: function (response) {
            console.log(response);
            $(street_id).val(response.logradouro);
            $(state_id).val(response.estado);
            $(city_id).val(response.cidade);
            $(neighborhood_id).val(response.bairro);
            $(latitude_id).val(response.latitude);
            $(longitude_id).val(response.longitude);
            $(cod_ibge_id).val(response.ibge);
        },
        error: function(response) {
            console.log(response);
        }
    });
});

// $("#submit_phone").on("click", function(event){
//     event.preventDefault();
//     var name = $('#id_name').val();
//     var number = $('#id_number').val();

//     var formData = new FormData();
//     formData.append('pk', politic_id);
//     formData.append('name', name);
//     formData.append('number', number);

//     $.ajax({
//         url: url_phone_create,
//         type: 'POST',
//         headers: {"X-CSRFToken": getCookie("csrftoken")},
//         data: formData,
//         async: false,
//         cache: false,
//         contentType: false,
//         enctype: 'multipart/form-data',
//         processData: false,
//         success: function (response) {
//             console.log(response);
//             var file_url = response.file_url;
//             var phone_key = response.phone_key;

//             var html = '<tr id="row-'+phone_key+'">';
//             html +=         '<td>';
//             html +=             name;
//             html +=         '</td>';
//             html +=         '<td>' + number + '</td>';
//             html +=         '<td>';
//             html +=             '<a class="delete_object" href="' + url_phone_delete + '" data-pk="'+ phone_key + '" data-row="#row-' + phone_key + '">';
//             html +=                 '<i class="glyphicon glyphicon-trash" style="color:#778899;"></i>';
//             html +=             '</a>';
//             html +=         '</td>';
//             html +=     '</tr>';
            
//             $("#table_phones").append(html);

//             $("#id_name").val('');
//             $("#id_number").val('');            
//         },
//         error: function(response) {
//             console.log(response);
//         }
//     });
// });

// $("#submit_extra_document").on("click", function(event){
//     event.preventDefault();
//     var extra_document = $('#id_extra_document').prop('files')[0];
//     var extra_description = $('#id_extra_description').val();

//     var formData = new FormData();
//     formData.append('pk', politic_id);
//     formData.append('extra_document', extra_document);
//     formData.append('extra_description', extra_description);

//     $.ajax({
//         url: url_document_create,
//         type: 'POST',
//         headers: {"X-CSRFToken": getCookie("csrftoken")},
//         data: formData,
//         async: false,
//         cache: false,
//         contentType: false,
//         enctype: 'multipart/form-data',
//         processData: false,
//         success: function (response) {
//             console.log(response);
//             var file_url = response.file_url;
//             var document_key = response.document_key;

//             var html = '<tr id="row-'+document_key+'">';
//             html +=         '<td>';
//             html +=             '<a target="_blank" href="' + file_url + '">';
//             html +=                 extra_document.name;
//             html +=             '</a>';
//             html +=         '</td>';
//             html +=         '<td>' + extra_description + '</td>';
//             html +=         '<td>';
//             html +=             '<a class="delete_object" href="' + url_document_delete + '" data-pk="'+ document_key + '" data-row="#row-' + document_key + '">';
//             html +=                 '<i class="glyphicon glyphicon-trash" style="color:#778899;"></i>';
//             html +=             '</a>';
//             html +=         '</td>';
//             html +=     '</tr>';
            
//             $("#table_extra_documents").append(html);

//             $("#id_extra_document").val('');
//             $("#id_extra_description").val('');            
//         },
//         error: function(response) {
//             console.log(response);
//         }
//     });
// });

// // Delete Confirmation phone
// $(".delete_phone").on('click', function(event){
//     event.preventDefault();
//     var phone_key = $(this).data('pk');
//     var row_id = $(this).data('row');
//     $.confirm({
//         title: 'DELETAR',
//         content: 'Tem certeza que deseja remover este telefone?',
//         buttons: {
//             confirm: {
//                 text: 'SIM',
//                 btnClass: 'btn-red',
//                 keys: ['enter'],
//                 theme: 'material',
//                 action: function(){
//                     var formData = new FormData();
//                     formData.append('phone_key', phone_key);
//                     $.ajax({
//                         url: url_phone_delete,
//                         type: 'POST',
//                         headers: {"X-CSRFToken": getCookie("csrftoken")},
//                         data: formData,
//                         async: false,
//                         cache: false,
//                         contentType: false,
//                         enctype: 'multipart/form-data',
//                         processData: false,
//                         success:function(response){
//                             console.log(response);
//                             $(row_id).remove();
//                         },
//                         error: function(response) {
//                             console.log(response);
//                         }
//                     })
//                 }   
//             },
//             cancel: {
//                 text: 'CANCELAR',
//                 btnClass: 'btn-gray',
//                 keys: ['escape'],
//                 theme: 'material'
//             }
//         }
//     });
// });

// // Delete Confirmation document
// $(".delete_document").on('click', function(event){
//     event.preventDefault();
//     var document_key = $(this).data('pk');
//     var row_id = $(this).data('row');
//     $.confirm({
//         title: 'DELETAR',
//         content: 'Tem certeza que deseja remover este documento?',
//         buttons: {
//             confirm: {
//                 text: 'SIM',
//                 btnClass: 'btn-red',
//                 keys: ['enter'],
//                 theme: 'material',
//                 action: function(){
//                     var formData = new FormData();
//                     formData.append('document_key', document_key);
//                     $.ajax({
//                         url: url_document_delete,
//                         type: 'POST',
//                         headers: {"X-CSRFToken": getCookie("csrftoken")},
//                         data: formData,
//                         async: false,
//                         cache: false,
//                         contentType: false,
//                         enctype: 'multipart/form-data',
//                         processData: false,
//                         success:function(response){
//                             console.log(response);
//                             $(row_id).remove();
//                         },
//                         error: function(response) {
//                             console.log(response);
//                         }
//                     })
//                 }   
//             },
//             cancel: {
//                 text: 'CANCELAR',
//                 btnClass: 'btn-gray',
//                 keys: ['escape'],
//                 theme: 'material'
//             }
//         }
//     });
// });
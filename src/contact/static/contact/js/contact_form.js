$(document).ready(function(){
    get_placeholder('#id_name', 321);
    get_placeholder('#id_email_c', 322);
    get_placeholder('#id_message', 323);
    $("#id_name").keyup(function(){
        $('#id_name_v').fadeOut('slow');
    });
    $("#id_email_c").keyup(function(){
        $('#id_email_v').fadeOut('slow');
    });
    $("#id_message").keyup(function(){
        $('#id_message_v').fadeOut('slow');
    });
    $('#submit_btn').click(function(e){
        var name = $.trim($('#id_name').val());
        var email = $.trim($('#id_email_c').val());
        var message = $.trim($('#id_message').val());
        var atpos = email.indexOf("@");
        var dotpos = email.lastIndexOf(".");
        if (name === '') {
            get_html_fadeIn('#id_name_v', 326, 0);
            return false;
        }
        if (email === '') {
            get_html_fadeIn('#id_email_v', 327, 0);
            return false;
        }
        if (email !== '' && atpos<1 || dotpos<atpos+2 || dotpos+2>=email.length) {
            get_html_fadeIn('#id_email_v', 328, 0);
            return false;
        }
        if (message === '') {
            get_html_fadeIn('#id_message_v', 329, 0);
            return false;
        }

        e.preventDefault();
        var url = url_contact;
        var data = $('#contactForm').serialize();
        fromSubmit(url, data);
    });

    var fromSubmit= function(url, data){
        var formData = new FormData($('#contactForm')[0]);
        $.ajax({
            type : "POST",
            url : url,
            dataType : "json",
            data : formData,
            success : function(data) {
                if(data.success_msg)
                {
                    get_html_fadeIn('.reply', 330, 1000);
                }
                if(data.error_msg)
                {
                    get_html_fadeIn('.reply', 331, 1000);
                }
                $('#contactForm')[0].reset();
                setTimeout(function(){
                    $('#modal_close_c').trigger('click');
                    $('.reply').fadeOut('slow');
                }, 3000);
            },
            cache: false,
            contentType: false,
            processData: false,
            error : function(XMLHttpRequest, textStatus, errorThrown) {
            }
        });
    };
});

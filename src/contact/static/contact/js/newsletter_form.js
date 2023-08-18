$(document).ready(function(){
    get_placeholder('#id_email_address', 322);
    $("#id_email_address").keyup(function(){
        $('#id_email_address_v').fadeOut('slow');
    });
    $('#subs_btn').click(function(e){
        var email_address = $.trim($('#id_email_address').val());
        var atpos = email_address.indexOf("@");
        var dotpos = email_address.lastIndexOf(".");
        if (email_address === '') {
            get_html_fadeIn('#id_email_address_v', 341, 0);
            return false;
        }
        if (email_address !== '' && atpos<1 || dotpos<atpos+2 || dotpos+2>=email_address.length) {
            get_html_fadeIn('#id_email_address_v', 342, 0);
            return false;
        }
        e.preventDefault();
        var url = url_newsletter;
        var data = $('#newsletter_form').serialize();
        fromSubmit(url, data);
    });

    var fromSubmit= function(url, data){
        $.ajax({
            type : "POST",
            url : url,
            dataType : "json",
            data : data,
            success : function(data) {
                if(data.success_msg)
                {
                    get_html_fadeIn('.subs_reply', 343, 1000);
                }
                if(data.error_msg)
                {
                    get_html_fadeIn('.subs_reply', 344, 1000);
                }
                $('#newsletter_form')[0].reset();
                setTimeout(function(){
                    $('#newsletter_modal_close').trigger('click');
                    $(".subs_reply").fadeOut('slow');
                }, 3000);

            },
            error : function(XMLHttpRequest, textStatus, errorThrown) {
            }
        });
    };
});

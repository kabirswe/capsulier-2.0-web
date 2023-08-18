
$( document ).ready(function() {

    $("#id_image1").change(function (e) {
        $image1.cropper("destroy");
        $('#crop_image1').html(image_not_save_yet);
        cropBoxData = null;
        canvasData = null;
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e){
                $("#image1").attr("src", e.target.result);
                $image1.cropper({
                    // aspectRatio: 1,
                    // viewMode: 1,
                    ready: function () {
                        $image1.cropper("setCanvasData", canvasData);
                        $image1.cropper("setCropBoxData", cropBoxData);
                        croppable = true;
                    }
                });
            };
            reader.readAsDataURL(this.files[0]);
        }
    });

    $('#crop_image1').click(function(e){
        e.preventDefault();
        var imageCheck = $('#id_image1').val();
        // console.log(imageCheck);
        if(imageCheck!=''){
            var cropData = $image1.cropper("getData");
            console.log($image1.cropper());
            console.log(cropData);
            // round canvas display
            var croppedCanvas;
            // var roundedCanvas;
            if (!croppable) {
                return;
            }
            // Crop
            croppedCanvas = $image1.cropper('getCroppedCanvas');
            $(".crop_display1").html('<img src="' + croppedCanvas.toDataURL() + '">');
            $("#id_x1").val(cropData["x"]);
            $("#id_y1").val(cropData["y"]);
            $("#id_height1").val(cropData["height"]);
            $("#id_width1").val(cropData["width"]);
            $('#crop_image1').html(image_save);
            // $image1.cropper("destroy");
            // $("#step7").trigger( "click" );
        }//image check
    });

    $('#crop_image1_clear').click(function(e) {
        e.preventDefault();
        $image1.cropper("clear", "true");
        $(".crop_display1").html('');
        $('#crop_image1').html(image_not_save_yet);
    });

    $(".img-zoom-in1").click(function () {
        $image1.cropper("zoom", 0.1);
    });

    $(".img-zoom-out1").click(function () {
        $image1.cropper("zoom", -0.1);
    });

    $(".img-reset1").click(function () {
        $image1.cropper("reset");
    });

    $(".img-rotate-451").click(function () {
        $image1.cropper("rotate", -45);
    });

    $(".img-rotate451").click(function () {
        $image1.cropper("rotate", 45);
    });



    $("#id_image").change(function (e) {
        $image.cropper("destroy");
        $('#crop_image').html(image_not_save_yet);
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e){
                $("#image2").attr("src", e.target.result);
                $image.cropper({
                    // aspectRatio: 1,
                    // viewMode: 1,
                    ready: function () {
                        // $image.cropper("setCanvasData", canvasData);
                        // $image.cropper("setCropBoxData", cropBoxData);
                        croppable = true;
                    }
                });
            };
            reader.readAsDataURL(this.files[0]);
        }
    });

    $('#crop_image').click(function(e){
        e.preventDefault();
        var imageCheck = $('#id_image').val();
        // console.log(imageCheck);
        if(imageCheck!=''){

            var cropData = $image.cropper("getData");
            console.log(cropData);
            // round canvas display
            var croppedCanvas;
            // var roundedCanvas;
            if (!croppable) {
                return;
            }
            // Crop
            croppedCanvas = $image.cropper('getCroppedCanvas');
            $("#crop_display").html('<img src="' + croppedCanvas.toDataURL() + '">');
            $(".crop_display2").html('<img src="' + croppedCanvas.toDataURL() + '">');
            $("#id_x").val(cropData["x"]);
            $("#id_y").val(cropData["y"]);
            $("#id_height").val(cropData["height"]);
            $("#id_width").val(cropData["width"]);
            $('#crop_image').html(image_save);
            // $image.cropper("destroy");
            // $("#step4").trigger("click");
        }//image check
    });

    $('#crop_image_clear').click(function(e) {
        e.preventDefault();
        $image.cropper("clear", "true");
        $("#image2").attr("src", "{% static 'mycaps/img/icons/crop-def.png' %}");
        $("#crop_display").html('');
        $(".crop_display2").html('');
        $('#crop_image').html(image_not_save_yet);
    });

    $(".img-zoom-in").click(function () {
        $image.cropper("zoom", 0.1);
    });

    $(".img-zoom-out").click(function () {
        $image.cropper("zoom", -0.1);
    });

    $(".img-reset").click(function () {
        $image.cropper("reset");
    });

    $(".img-rotate-45").click(function () {
        $image.cropper("rotate", -45);
    });

    $(".img-rotate45").click(function () {
        $image.cropper("rotate", 45);
    });
});

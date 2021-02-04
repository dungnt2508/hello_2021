$("form[name=register_form]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/auth/register",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp)
            window.location.href = "/";
        },
        error: function(resp){
            console.log(resp)
            $error.html(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
});

$("form[name=login_form]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/auth/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp)
            window.location.href = "/";
        },
        error: function(resp){
            console.log(resp)
            $error.html(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
})
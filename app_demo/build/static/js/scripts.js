$("form[name=register_form]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/register",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp)
            window.location.href = "/user/login";
        },
        error: function(resp){
            console.log(resp)
            $error.html(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
});


$("form[name=register_form_nv]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/create/1",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp)
            window.location.href = "/user/filter";
        },
        error: function(resp){
            console.log(resp)
            $error.html(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
});

$("form[name=register_form_customer]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/create/2",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp)
            window.location.href = "/customer/list";
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
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp)
            window.location.href = "/page/dashboard";
        },
        error: function(resp){
            console.log(resp)
            $error.html(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
})


$("form[name=invoice_pawn]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    console.log(data)

    $.ajax({
        url: "/invoice/create",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp)
            window.location.href = "/page/dashboard";
        },
        error: function(resp){
            console.log(resp)
            $error.html(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
})


$("#item_kind").on("change",function(e){
        $("#from_date").val("");
        $("#to_date").val("");
        $("#price_rate").val("");
        $("#week").val("");

        var kind_item = $.parseJSON(this.value);

        $.ajax({
            url: "/setting/get_rate/"+kind_item.toString(),
            type: "GET",
            data: kind_item,
            dataType: "json",
            success: function(resp){
                console.log(kind_item)
                console.log(resp)
                $("#rate").val(resp/4);
                $("#kind_item").val(kind_item);

            },
            error: function(resp){
                console.log(resp)

            }
        })


    });


$("#to_date").on("change",function(e){
        //Getting Value
        var item_kind = $("#item_kind").val();
        if(item_kind.length == 0){
            alert("Bạn cần chọn loại tài sản để hệ thống tính lãi !")
            $("#to_date").val("");
            return
        }

        var price = $("#price").val()
        if(price.length == 0){
            alert("Bạn cần nhập số tiền vay để hệ thống tính lãi !")
            $("#to_date").val("");
            return
        }

        var from_date = $("#from_date").val();
        if(from_date.length == 0){
            alert("Bạn cần nhập ngày vay để hệ thống tính lãi")
            $("#to_date").val("");
            return
        }

        var to_date = $("#to_date").val()


        var startDay = new Date(from_date);
        var endDay = new Date(to_date);
        var millisBetween = endDay.getTime() - startDay.getTime();
        var days = 1 + (millisBetween / (1000 * 3600 * 24));
        if(days <=0 ){
            alert("Ngày vay không thể nhỏ hơn ngày đến hạn trả lãi")
            $("#from_date").val("");
            $("#to_date").val("");
            $("#price_rate").val("");
            $("#week").val("");
            return
        }
        if(days > 0 ){
            var week = 1
            var check_day = days % 7
            console.log(check_day)

            if(check_day == 0){
                week = Math.floor(days/7)
            }
            else{
                week = Math.floor(days/7) + 1
            }

            var rate = $("#rate").val();
            var rate_pawn = price * (week * rate/100)

            $("#week").val(week);
            $("#price_rate").val(rate_pawn);
        }

    });

$("#from_date").on("change",function(e){
        //Getting Value
        var price_rate = $("#price_rate").val();
        if(price_rate.length != 0){
            $("#to_date").val("");
            $("#price_rate").val("");
            $("#week").val("");
        }

    });

$("#price").on("change",function(e){
        //Getting Value
        var price_rate = $("#price_rate").val();
        if(price_rate.length != 0){
            $("#from_date").val("");
            $("#to_date").val("");
            $("#price_rate").val("");
            $("#week").val("");
        }

    });

$("form[name=funds_collect]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/funds/collect",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp)
            window.location.href = "/page/dashboard";
        },
        error: function(resp){
            console.log(resp)
            $error.html(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
});

$("form[name=funds_spent]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/funds/spent",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp)
            window.location.href = "/page/dashboard";
        },
        error: function(resp){
            console.log(resp)
            $error.html(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
});

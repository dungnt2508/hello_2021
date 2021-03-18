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


$("#pawn_item_kind").on("change",function(e){
        $("#pawn_from_date").val("");
        $("#pawn_to_date").val("");
        $("#pawn_price_rate").val("");
        $("#pawn_week").val("");

        var kind_item = $.parseJSON(this.value);

        $.ajax({
            url: "/setting/get_rate/"+kind_item.toString(),
            type: "GET",
            data: kind_item,
            dataType: "json",
            success: function(resp){
                console.log(kind_item)
                console.log(resp)
                $("#pawn_rate").val(resp/4);
                $("#pawn_kind_item").val(kind_item);

            },
            error: function(resp){
                console.log(resp)

            }
        })


    });


$("#pawn_to_date").on("change",function(e){
        //Getting Value
        var item_kind = $("#pawn_item_kind").val();
        if(item_kind.length == 0){
            alert("Bạn cần chọn loại tài sản để hệ thống tính lãi !")
            $("#pawn_to_date").val("");
            return
        }

        var price = $("#pawn_price").val()
        if(price.length == 0){
            alert("Bạn cần nhập số tiền vay để hệ thống tính lãi !")
            $("#pawn_to_date").val("");
            return
        }

        var from_date = $("#pawn_from_date").val();
        if(from_date.length == 0){
            alert("Bạn cần nhập ngày vay để hệ thống tính lãi")
            $("#pawn_to_date").val("");
            return
        }

        var to_date = $("#pawn_to_date").val()


        var startDay = new Date(from_date);
        var endDay = new Date(to_date);
        var millisBetween = endDay.getTime() - startDay.getTime();
        var days = 1 + (millisBetween / (1000 * 3600 * 24));
        if(days <=0 ){
            alert("Ngày vay không thể nhỏ hơn ngày đến hạn trả lãi")
            $("#pawn_from_date").val("");
            $("#pawn_to_date").val("");
            $("#pawn_price_rate").val("");
            $("#pawn_week").val("");
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

            var rate = $("#pawn_rate").val();
            var rate_pawn = price * (week * rate/100)

            $("#pawn_week").val(week);
            $("#pawn_price_rate").val(rate_pawn);
        }

    });

$("#pawn_from_date").on("change",function(e){
        //Getting Value
        var price_rate = $("#pawn_price_rate").val();
        if(price_rate.length != 0){
            $("#pawn_to_date").val("");
            $("#pawn_price_rate").val("");
            $("#pawn_week").val("");
        }

    });

$("#pawn_price").on("change",function(e){
        //Getting Value
        var price_rate = $("#pawn_price_rate").val();
        if(price_rate.length != 0){
            $("#pawn_from_date").val("");
            $("#pawn_to_date").val("");
            $("#pawn_price_rate").val("");
            $("#pawn_week").val("");
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


$("form[name=invoice_pay]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    console.log(data)

    $.ajax({
        url: "/invoice/pay",
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


$("#pay_id").on("input",function(e){
        $("#pay_name").val("");
        $("#pay_phone").val("");
        $("#pay_email").val("");
        $("#pay_cmnd").val("");
        $("#pay_address").val("");
        $("#pay_item_kind").val("");
        $("#pay_item_name").val("");
        $("#pay_from_date").val("");
        $("#pay_to_date").val("");
        $("#pay_rate").val("");
        $("#pay_week").val("");
        $("#pay_price").val("");
        $("#pay_price_rate").val("");

        var pay_id = $(this).val().replace(" ","")

        if(pay_id.length > 6){
            $.ajax({
                url: "/invoice/filter_one/"+pay_id,
                type: "GET",
                dataType: "json",
                success: function(resp){
                    $("#pay_name").val(resp.customer.name);
                    $("#pay_phone").val(resp.customer.phone);
                    $("#pay_email").val(resp.customer.email);
                    $("#pay_cmnd").val(resp.customer.cmnd);
                    $("#pay_address").val(resp.customer.address);
                    $("#pay_item_kind").val(resp.item_kind);
                    $("#pay_item_name").val(resp.item_name);
                    $("#pay_from_date").val(resp.from_date);
                    $("#pay_to_date").val(resp.to_date);
                    $("#pay_rate").val(resp.rate);
                    $("#pay_week").val(resp.week);
                    $("#pay_price").val(resp.price_pawn);
                    $("#pay_price_rate").val(resp.price_rate);
                },
                error: function(resp){
                    console.log(resp)

                }
            })
        }
    });

$("#redeem_id").on("input",function(e){
        $("#redeem_name").val("");
        $("#redeem_phone").val("");
        $("#redeem_email").val("");
        $("#redeem_cmnd").val("");
        $("#redeem_address").val("");
        $("#redeem_item_kind").val("");
        $("#redeem_item_name").val("");
        $("#redeem_from_date").val("");
        $("#redeem_to_date").val("");
        $("#redeem_rate").val("");
        $("#redeem_week").val("");
        $("#redeem_price").val("");
        $("#redeem_price_rate").val("");

        var redeem_id = $(this).val().replace(" ","")

        if(redeem_id.length > 6){
            $.ajax({
                url: "/invoice/filter_one/"+redeem_id,
                type: "GET",
                dataType: "json",
                success: function(resp){
                    $("#redeem_name").val(resp.customer.name);
                    $("#redeem_phone").val(resp.customer.phone);
                    $("#redeem_email").val(resp.customer.email);
                    $("#redeem_cmnd").val(resp.customer.cmnd);
                    $("#redeem_address").val(resp.customer.address);
                    $("#redeem_item_kind").val(resp.item_kind);
                    $("#redeem_item_name").val(resp.item_name);
                    $("#redeem_from_date").val(resp.from_date);
                    $("#redeem_to_date").val(resp.to_date);
                    $("#redeem_rate").val(resp.rate);
                    $("#redeem_week").val(resp.week);
                    $("#redeem_price").val(resp.price_pawn);
                    $("#redeem_price_rate").val(resp.price_rate);
                },
                error: function(resp){
                    console.log(resp)

                }
            })
        }
    });

$("form[name=invoice_redeem]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    console.log(data)

    $.ajax({
        url: "/invoice/redeem",
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
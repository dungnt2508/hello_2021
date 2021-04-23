//F đăng ký
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


// F đăng ký nhân viên
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


// F đăng ký khách hàng
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


// F đăng nhập
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



// F vay
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
//            readTextFile();

            window.open(
                  "/page/get_invoice/"+resp.invoice_id ,
                  '_blank' // <- This is what makes it open in a new window.

            );
            window.location.href = "/page/dashboard" ;
        },
        error: function(resp){
            console.log(resp)
            $error.html(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
})



// 20210408: Add Function to load html template and export
/*Function Print_Invoice_Bill()
{
var myBlob;

    doc.fromHTML($('#content').html(), 15, 15, {
        'width': 170,
            'elementHandlers': specialElementHandlers
    });
    myBlob = doc.save('blob');

}*/
//function test2()
//{
//
//
//   var reader = new XMLHttpRequest() || new ActiveXObject('MSXML2.XMLHTTP');
//   reader.open('get', 'http://localhost/test/hopdong_v1.txt', true);
//    //reader.onreadystatechange = displayContents;
//    //reader.send(null);
//    alert(reader.responseText);
//}


//function test()
//{
//    var rawFile = new XMLHttpRequest();
//
//
//    rawFile.open("GET", "file:///D:/Project/CamDoVietGold/vietgold_app/app_demo/build/templates/page/hopdong_v1.txt");
//
//    rawFile.onreadystatechange = function ()
//    {
//        if(rawFile.readyState === 4)
//        {
//            if(rawFile.status === 200 || rawFile.status == 0)
//            {
//                var allText = rawFile.responseText;
//                alert(allText);
//            }
//        }
//    }
//    rawFile.send(null);
//}

$("#pawn_item_kind").on("change",function(e){
        $("#pawn_from_date").val("");
        $("#pawn_to_date").val("");
        $("#pawn_price_rate").val("");
        $("#pawn_week").val("");
        $("#detail_rate").val("");

        var kind_item = $.parseJSON(this.value);

        $.ajax({
            url: "/setting/get_rate_kind_item/"+kind_item.toString(),
            type: "GET",
            data: kind_item,
            dataType: "json",
            success: function(resp){
                //console.log(kind_item)
                //console.log(resp)
                $("#pawn_rate").val((parseInt(resp.rate) + parseInt(resp.service_charge) + parseInt(resp.storage_charge))/4);
                $("#detail_rate").val("-Lãi suất :" + resp.rate + "%" + " -Phí dịch vụ : " + resp.service_charge + "%" + " -Phí bảo quản : " + resp.storage_charge + "%");
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

        var price = $("#pawn_price").val().replaceAll(',', '')
        console.log(price)
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
            //console.log(check_day)

            if(check_day == 0){
                week = Math.floor(days/7)
            }
            else{
                week = Math.floor(days/7) + 1
            }
            var rate = $("#pawn_rate").val()
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
                    console.log(resp)
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
        console.log("redeem_id",e);
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

$("#upd_kind_item").on("input",function(e){

        $("#upd_item_name").val("");
        $("#upd_rate").val("");
        $("#upd_service_charge").val("");
        $("#upd_storage_charge").val("");

        var upd_kind_item = $(this).val().replace(" ","")

        if(upd_kind_item.length > 0){
            $.ajax({
                url: "/setting/set_rate/"+upd_kind_item,
                type: "GET",
                dataType: "json",
                success: function(resp){
                    console.log(resp)
                    $("#upd_item_name").val(resp.item_name);
                    $("#upd_rate").val(resp.rate);
                    $("#upd_service_charge").val(resp.service_charge);
                    $("#upd_storage_charge").val(resp.storage_charge);
                    console.log(resp)
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

$("form[name=update_rate]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/setting/update_rate/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp)
            window.location.href = "/setting/filter_rate";
        },
        error: function(resp){
            console.log(resp)
            $error.html(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
})
//------Format Numner

$("input[data-type='currency']").on({
    keyup: function() {
      formatCurrency($(this));
    },
    blur: function() {
      formatCurrency($(this), "blur");
    }
});


function formatNumber(n) {
  // format number 1000000 to 1,234,567
  return n.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}


function formatCurrency(input, blur) {
  // appends $ to value, validates decimal side
  // and puts cursor back in right position.

  // get input value
  var input_val = input.val();

  // don't validate empty input
  if (input_val === "") { return; }

  // original length
  var original_len = input_val.length;

  // initial caret position
  var caret_pos = input.prop("selectionStart");

  // check for decimal
  if (input_val.indexOf(".") >= 0) {

    // get position of first decimal
    // this prevents multiple decimals from
    // being entered
    var decimal_pos = input_val.indexOf(".");

    // split number by decimal point
    var left_side = input_val.substring(0, decimal_pos);
    var right_side = input_val.substring(decimal_pos);

    // add commas to left side of number
    left_side = formatNumber(left_side);

    // validate right side
    right_side = formatNumber(right_side);

    // On blur make sure 2 numbers after decimal
    if (blur === "blur") {
      right_side += "00";
    }

    // Limit decimal to only 2 digits
    right_side = right_side.substring(0, 2);

    // join number by .
    input_val = "" + left_side + "." + right_side;

  } else {
    // no decimal entered
    // add commas to number
    // remove all non-digits
    input_val = formatNumber(input_val);
    input_val = input_val;

    // final formatting
    if (blur === "blur") {
      //input_val += ".00";
    }
  }

  // send updated string to input
  input.val(input_val);

  // put caret back in the right position
  var updated_len = input_val.length;
  caret_pos = updated_len - original_len + caret_pos;
  input[0].setSelectionRange(caret_pos, caret_pos);
}



//------Format Numner

function cms_pay(invoice_id) {
//    alert(invoice_id)
    window.location.href = "/invoice/pay/"+invoice_id
}

function cms_redeem(invoice_id) {
//    alert(invoice_id)
    window.location.href = "/invoice/redeem/"+invoice_id;
}



$( document ).ready(function() {
    var url = window.location.pathname;
    var id = url.substring(url.lastIndexOf('/') + 1);
    url_pay = "/invoice/pay/"+id
    url_redeem = "/invoice/redeem/"+id
//    url_rate = "/setting/set_rate/"+id
    console.log(url)
    console.log(id)
    if(url == url_pay){
        $("#pay_id").val(id);
        $.ajax({
                    url: "/invoice/filter_one/"+id,
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
    };
    if(url == url_redeem){
        $("#redeem_id").val(id);
        $.ajax({
                    url: "/invoice/filter_one/"+id,
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
    };
});

$("#redeem_week_real").on("input",function(e){
        console.log("redeem_week_real",e);
        var redeem_week = $("#redeem_week").val();
        var redeem_price_rate = $("#redeem_price_rate").val().replaceAll(',', '');
        var redeem_week_real = $(this).val();
        var redeem_price_rate_real = (redeem_price_rate/redeem_week) * redeem_week_real;

        if (redeem_week_real == 0 || redeem_week_real.length == 0){
            $("#redeem_price_rate_real").val(redeem_price_rate);
        }
        else {
            $("#redeem_price_rate_real").val(redeem_price_rate_real);
        }

    });



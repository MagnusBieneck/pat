function toggleAccountDetails() {
    if ($("#id_refund_type").val() === "bank_account") {
        $(".bank-account-details").show();
    } else {
        $(".bank-account-details").hide();
    }
}

function showNextReceipt(){
    let lastVisibleReceipt = 1;

    for(let i = 0; i < 9; i++) {
        console.log(i);

        if ($(".receipt-" + i).is(":visible")) {
            lastVisibleReceipt = i;
        }else{
            break;
        }
    }

    $(".receipt-" + parseInt(lastVisibleReceipt + 1)).show();

    if(lastVisibleReceipt === 8){
        $("#btn_show_next_receipt").hide();
    }
}

function calculateSum(){
    let sum = 0;

    for(let i = 0; i <= 9; i++){
        let value = $("#id_receipt_" + i + "_amount").val();
        value = value.replace(",", ".");

        sum += parseFloat(value);
    }

    $("#span_amount_total").html(sum.toFixed(2).replace(".", ","));
}

// Initially, hide all receipt fields but one
$(document).ready(function () {
    $(".receipt-1").hide();
    $(".receipt-2").hide();
    $(".receipt-3").hide();
    $(".receipt-4").hide();
    $(".receipt-5").hide();
    $(".receipt-6").hide();
    $(".receipt-7").hide();
    $(".receipt-8").hide();
    $(".receipt-9").hide();

    toggleAccountDetails();
    calculateSum();

    $("#id_refund_type").change(function(){
        toggleAccountDetails();
    });

    $(".textinput").on("input", function(){
        calculateSum();
    })
});
function passToModal(element) {
    // To remove the click handler, if they click on multiple phases, otherwise they run `n` times
    $("#confirm").unbind("click");
    const confirmB = document.getElementById("confirm");
    confirmB.innerHTML = "Yank train, Phase " + element.getAttribute('data-id');
    $("#confirm").click(function (e) {
        e.preventDefault();
        const loaderTransitionTime = document.querySelector("#loader");
        const loader2TransitionTime = document.querySelector("#loader2");
        let duration = Math.random() * 8000;
        loaderTransitionTime.style.setProperty("animation-duration", duration + "ms");
        loader2TransitionTime.style.setProperty("animation-duration", duration + "ms");
        $('#loader').show();
        $("#confirm").attr("disabled", true);
        $("#deny").attr("disabled", true);
        $.ajax({
            type: "POST",
            url: "/run_phase",
            data: {
                id: element.getAttribute('data-id'),
            },
            success: function (result) {
                // Parse the result array
                result = JSON.parse(result);
                let errors = [];
                for (let i = 0; i < result.length; i++) {
                    if (result[i] == "Queries Completed Successfully") {
                        // Do nothing
                    } else {
                        errors.push(result[i]);
                    }
                }
                $('#loader').hide();
                if (errors.length == 0) {
                    $('#alert_placeholder').html('<div class="alert alert-success alert-dismissible fade show" role="alert"><strong>Holy guacamole!</strong> ' + "Queries Completed Successfully" + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>');
                } else {
                    let errors_string = "";
                    console.log(errors_string);
                    for (let i = 0; i < errors.length; i++) {
                        errors_string = errors_string + ('<div>' + errors[i] + '</div><hr>');
                    }
                    $('#alert_placeholder').html('<div class="alert alert-danger alert-dismissible fade show" role="alert"><strong>JA JA JA</strong> ' + errors_string + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>');
                }
                $("#confirm").attr("disabled", false);
                $("#deny").attr("disabled", false);
                $("#exampleModal .close").click();
            },
            error: function (result) {
                $('#alert_placeholder').html('<div class="alert alert-danger alert-dismissible fade show" role="alert"><strong>JA JA JA</strong> ' + result + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>');
                $("#exampleModal .close").click();
            }
        });
    });
}

function create_mod() {
    $.ajax({
        url: '/receive-teaches-mod',
        type: 'post',
        data: $('#createMod').serialize(),
        success: function (result) {
            if (result == "Query Completed Successfully") {
                $('#alert_placeholder_mod').html('<div class="alert alert-success alert-dismissible fade show" role="alert"><strong>Holy guacamole!</strong> ' + result + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>');
                $.get("/get_mod_selection", function (data) {
                    $('#teach').html(data);
                });
                $('#teach').val('');
                $('#modToPair').val('');
            } else {
                $('#alert_placeholder_mod').html('<div class="alert alert-danger alert-dismissible fade show" role="alert"><strong>JA JA JA JA</strong> ' + result + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>');
            }
        },
        error: function (result) {
            alert(result);
        }
    });
    return false;
}

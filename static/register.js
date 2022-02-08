$("#submit").click(function () {

    var name = $("#name").val();
    var email = $("#email").val();
    var pass = $("#pass").val();
    var pass1 = $("#pass1").val();

    setTimeout(function() {

        if (name != '' && email != '' && pass != '' && pass1 != '') {

            swal({
              title: "Register completed!",
              text: "You have registered!",
              icon: "success",
              button: "ok",
            });
        }

    }, 2000);

});
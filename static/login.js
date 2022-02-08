$("#submit").click(function () {

    var email = $("#email").val();
    var pass = $("#pass").val();

    setTimeout(function() {

        if (email != '' && pass != '') {

            swal({
              title: "Login completed!",
              text: "You have logged in!",
              icon: "success",
              button: "ok",
            });
        }

    }, 1500);

});
function submitRatings() {
    var form = document.getElementsByName('stars');
    for (i = 0; i < form.length; i++) {
        if (form[i].checked) {
            console.log(form[i].value);
            document.forms["rating"].submit();
        }
    }
}
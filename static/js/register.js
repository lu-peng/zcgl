$(function () {
    alert('hello');
    commit();
})

function commit(request) {
    $('#registerbtn').click(function () {
        $('.modal').modal('show');
    });
}
$(function () {
    $('#inlineFormInputSearchTargetType').keyup(function () {

        $.ajax({
            type: "POST",
            url: "/search/",
            data: {
                'target_type_search_text': $('#inlineFormInputSearchTargetType').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchTargetTypeSuccess,
            dataType: 'html'
        });
    });

    // var latitude;
    // var longitude;
    //
    // $('#currentLocationAddon').click(function () {
    //     alert("clicked");
    //     getLocation();
    //     alert(latitude);
    //     alert(longitude);
    // })

});

function searchTargetTypeSuccess(data, textStatus, jqXHR) {
    $('#contractor-search-results').html(data)
}

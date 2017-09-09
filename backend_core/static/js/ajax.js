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


//     var latitude, longitude;
//
//
//
// function getLocation() {
//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(showPosition);
//     } else {
//             alert("Geolocation is not supported by this browser.");
//     }
// }
//
// function showPosition(position) {
//     latitude = position.coords.latitude;
//     longitude = position.coords.longitude;
// }
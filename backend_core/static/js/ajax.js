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
});

function searchTargetTypeSuccess(data, textStatus, jqXHR) {
    $('#contractor-search-results').html(data)
}
// $(function () {
//
//     $('#inlineFormInputSearchTargetType').keyup(function () {
//
//         $.ajax({
//             type: "POST",
//             url: "/search/",
//             data: {
//                 'target_type_search_text': $('#inlineFormInputSearchTargetType').val(),
//                 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
//             },
//             success: searchTargetTypeSuccess,
//             dataType: 'html'
//         });
//     });
// });

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) {
                c_end = document.cookie.length;
            }
            return decodeURI(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

function searchTargetTypeSuccess(data, textStatus, jqXHR) {
    $('#contractor-search-results').html(data)
}

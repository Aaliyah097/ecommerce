get_categories();

function get_categories(){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax(
         {
             type: 'get',
             url: '/catalog/categories',
             headers: {'X-CSRFToken': csrf_token},
             mode: 'same-origin',
             async: true,
             success : function(json)
             {
               document.write(json);
             },
             error : function(xhr,errmsg,err) {
                console.log(errmsg);
             }
         }
     )
}
class Brand{
    constructor(name, slug, image_url){
        this.name = name;
        this.slug = slug;
        this.image_url = image_url;
    }
}

class Brands{
    constructor() {
        this.collection = [];
        this.concrete_brand = null;
        this.url = '/catalog/brands/';
    }

    select(brand){
        this.concrete_brand = brand;
    }

    delete() {
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax(
            {
                type: 'delete',
                url: this.url + this.concrete_brand.slug,
                headers: {'X-CSRFToken': csrf_token},
                mode: 'same-origin',
                async: false,
                success: function (response) {

                },
                error: function (xhr, errmsg, err) {
                    alert([xhr, errmsg, err]);
                }
            }
        )
        this.concrete_brand = null;
    }

    update(form_data){
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax(
            {
                type: 'patch',
                data: form,
                url: this.url,
                headers: {'X-CSRFToken': csrf_token},
                contentType: 'multipart/form-data',
                mode: 'same-origin',
                async: false,
                success : function(response)
                {

                },
                error : function(xhr,errmsg,err) {
                    console.log(errmsg);
                }
            }
        )
    }

    create(form_data){
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax(
            {
                type: 'post',
                data: form,
                url: this.url,
                headers: {'X-CSRFToken': csrf_token},
                mode: 'same-origin',
                async: false,
                success : function(response)
                {

                },
                error : function(xhr,errmsg,err) {
                    console.log(errmsg);
                }
            }
        )
    }

    get_all(){
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        let brands = $.ajax(
            {
                type: 'get',
                url: this.url,
                headers: {'X-CSRFToken': csrf_token},
                mode: 'same-origin',
                async: false,
                success : function(response)
                {
                    return response;
                },
                error : function(xhr,errmsg,err) {
                    console.log(errmsg);
                }
            }
        )

        brands.responseJSON.forEach((brand) => {
            this.collection.push(
                new Brand(
                    brand.name,
                    brand.slug,
                    brand.file
                )
            )
        })
    }
}

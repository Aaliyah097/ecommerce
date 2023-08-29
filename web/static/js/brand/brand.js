class Brand{
    constructor(name, slug, image_url){
        this.name = name;
        this.slug = slug;
        this.image_url = image_url;
    }
}

class BrandRepository{
    constructor() {
        this.collection = [];
        this.concrete_brand = null;
        this.url = '/catalog/brands/';
        this.get_all();
    }

    select(brand_slug){
        console.log(this.collection.filter(
            item=>item.slug === brand_slug
        ));
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


class BrandView{
    constructor() {
        this.repository = new BrandRepository();
    }
    form(){
        let form = document.createElement('form');
        form.id = "brand_form";

        let fields = ["name", "slug", "file"]

        fields.forEach((field_name)=>{
            let input_el = document.createElement('input');
            input_el.name = field_name;
            input_el.id = form.id + "_" + field_name
            input_el.type = "text";

            let label_el = document.createElement("label");
            label_el.innerText = field_name.toUpperCase();
            label_el.setAttribute("for", input_el.id)

            form.insertAdjacentElement('beforeend', label_el);
            form.insertAdjacentElement('beforeend', input_el);
        })

        return form
    }
    selector(){
        let select = document.createElement('select');
        select.id = "brand_selector";
        select.setAttribute('v-model', 'current_el');
        this.repository.collection.forEach((brand)=>{
            let option = document.createElement('option');
            option.text = brand.name;
            option.value = brand.slug;
            select.insertAdjacentElement('beforeend', option);
        })
        return select
    }
}

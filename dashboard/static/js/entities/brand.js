const BRAND_URL = '/catalog/brands/';
const CSRF_TOKEN = $('input[name="csrfmiddlewaretoken"]').val();


class Brand extends IModel{
    static fields = {
        'slug': String.name,
        'name': String.name,
        'file': Image.name
    }
    static pk_field = 'slug';
    static display_field = 'name';
}

let brand_repo = new IRepo(Brand, BRAND_URL, CSRF_TOKEN);

let brand_view = new IView(brand_repo);

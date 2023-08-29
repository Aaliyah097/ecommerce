/*
* Example
*
* const BRAND_URL = '/catalog/brands/';
*
* const CSRF_TOKEN = $('input[name="csrfmiddlewaretoken"]').val();
*
* class Brand extends IModel{static fields = ['name', 'slug', 'file'];}
*
* let repo = new IRepo(Brand, BRAND_URL, CSRF_TOKEN);
*
* let brands = repo.list();
*
* console.log(brands);
*
* */


/*
* @property {Array[string]} fields
*/
class IModel{
    static fields = [];
    constructor(...args) {
        let counter = 0;
        args.forEach((arg)=>{
            this[this.constructor.fields[counter]] = arg;
            counter += 1;
        })
    }
}

/*
* @param {Class} model
* @param {String} base_url
* @parm {String} token
*/
class IRepo{
    constructor(model, base_url, token) {
        this.model = model;
        this.fields = model.fields;
        this.base_url = base_url;
        this.token = token;
    }
    /*
    * @param {String} pk
    */
    delete(pk){
        $.ajax(
            {
                type: 'DELETE',
                url: this.base_url + String(pk),
                headers: {'X-CSRFToken': this.token},
                mode: 'same-origin',
                async: true,
                success: function () {
                    alert('Deleted OK');
                },
                error: function (xhr, errmsg, err) {
                    alert([xhr, errmsg, err]);
                }
            }
        )
    }
    /*
    * @param {Form | FormData} form
    * => String
    * */
    get_content_type(form){
        if (form instanceof  FormData){
            return 'multipart/form-data';
        }
        else{
            return 'application/json';
        }
    }
    /*
    * @param {String} pk
    * @param {Form | FormData} form
    */
    update(pk, form){
        $.ajax(
            {
                type: 'PATCH',
                data: form,
                url: this.base_url + String(pk),
                headers: {'X-CSRFToken': this.token},
                contentType: this.get_content_type(form),
                mode: 'same-origin',
                async: true,
                success : function(response)
                {
                    alert('Updated OK');
                },
                error : function(xhr,errmsg,err) {
                    alert([xhr, errmsg, err]);
                }
            }
        )
    }
    /*
    * @param {Form | FormData} form
    * */
    create(form){
        $.ajax(
            {
                type: 'POST',
                data: form,
                url: this.base_url,
                headers: {'X-CSRFToken': this.token},
                contentType: this.get_content_type(form),
                mode: 'same-origin',
                async: true,
                success : function(response)
                {
                    alert('Created OK');
                },
                error : function(xhr,errmsg,err) {
                    alert([xhr, errmsg, err]);
                }
            }
        )
    }
    /*
    * => Array[object {IModel}]
    * */
    list(){
        let models = $.ajax(
            {
                type: 'GET',
                url: this.base_url,
                headers: {'X-CSRFToken': this.token},
                mode: 'same-origin',
                async: false,
                success : function(response)
                {
                    return response;
                },
                error : function(xhr,errmsg,err) {
                    alert([xhr, errmsg, err]);
                }
            }
        )
        let collection = [];

        models.responseJSON.forEach((model) => {
            collection.push(
                new this.model(
                    ...Object.values(model)
                )
            )
        })
        return collection
    }
    /*
    * @param {String} pk
    * => object {IModel}
    * */
    retrieve(pk){
        let model = $.ajax(
            {
                type: 'GET',
                url: this.base_url + String(pk),
                headers: {'X-CSRFToken': this.token},
                mode: 'same-origin',
                async: false,
                success : function(response)
                {
                    return response;
                },
                error : function(xhr,errmsg,err) {
                    alert([xhr, errmsg, err]);
                }
            }
        )

        return new this.model(...Object.values(model))
    }
}

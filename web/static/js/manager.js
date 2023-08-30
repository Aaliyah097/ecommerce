/*
* Example
*
* const BRAND_URL = '/catalog/brands/';
*
* const CSRF_TOKEN = $('input[name="csrfmiddlewaretoken"]').val();
*
* class Brand extends IModel{
*   static fields = ['name', 'slug', 'file'];
*   pk_field = 'slug';
*   display_field = 'name';
* }
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
* @property {String} pk_field
* @property {String} display_field
*/
class IModel{
    static fields = [];
    static pk_field = null;
    static display_field = null;

    constructor(...args) {
        let fields = this.constructor.fields.sort();

        let counter = 0;
        args.forEach((arg)=>{
            this[fields[counter]] = arg;
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
            let sorted_keys = Object.keys(model).sort();
            let sorted_values = sorted_keys.map(key => model[key]);

            collection.push(
                new this.model(
                    ...sorted_values
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

        return new this.model(...Object.values(model).sort())
    }
}

/*
* @param {IRepo} repo
* */
class IView{
    constructor(repo) {
        this.repo = repo;
        this.selector_id = String(repo.model.name) + "_selector";
        this.form_id = String(repo.model.name) + "_form";
        this.table_id = String(repo.model.name) + "_table";
    }
    selector(){
        let select = document.createElement("select");
        select.id = this.selector_id;

        this.repo.list().forEach((model)=>{
            let option = document.createElement("option");
            option.text = model[this.repo.model.display_field];
            option.value = model[this.repo.model.pk_field];
            select.appendChild(option)
        })

        return select;
    }
    form(){
        let form = document.createElement("form");
        form.setAttribute('id', this.form_id);

        this.repo.model.fields.forEach(field_name=>{
            let span = document.createElement("span");
            span.textContent = field_name;

            let input = document.createElement("input");
            input.setAttribute('type', 'text');
            input.name = field_name;

            form.appendChild(span);
            form.appendChild(input);
        })

        let button = document.createElement("button");
        button.setAttribute('type', 'button');
        button.textContent = "Подтвердить";
        button.setAttribute("class", "btn btn-success");

        form.appendChild(button);

        return form
    }
    table_row(model){
        // row
        let row = document.createElement("tr");
        let td = document.createElement("td");

        // checkbox
        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        td.appendChild(checkbox);
        row.appendChild(td);

        // content
        this.repo.model.fields.forEach((field)=>{
            let td = document.createElement("td");
            td.textContent = model[field];
            row.appendChild(td);
        })

        return row;
    }
    table() {
        if (document.getElementById(this.table_id)){
            throw new Error(`element with id: ${this.table_id} already exists`);
        }
        // table
        let table = document.createElement("table");
        table.setAttribute('id', this.table_id);
        table.setAttribute('class', 'table');

        let thead = table.createTHead();
        let headerRow = thead.insertRow();

        //checkbox
        let th = document.createElement("th");
        headerRow.appendChild(th);

        // header
        this.repo.model.fields.sort().forEach(field_name=>{
            let th = document.createElement("th");
            th.textContent = field_name;
            headerRow.appendChild(th);
        })

        // body
        let tbody = table.createTBody();

        this.repo.list().forEach((model)=>{
            tbody.appendChild(this.table_row(model));
        });

        return table
    }
}
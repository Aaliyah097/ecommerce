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
* @property {Object[string, T]} fields
* @property {String} pk_field
* @property {String} display_field
*/
class IModel{
    static fields = {};
    static pk_field = null;
    static display_field = null;

    constructor(...args) {
        let fields = Object.keys(this.constructor.fields).sort();

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
        this.collection = this.list();
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
                    window.location.href = window.location.href;
                },
                error : function(xhr, status, error) {
                    alert(xhr.responseText);
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
                url: this.base_url + String(pk) + "/",
                headers: {'X-CSRFToken': this.token},
                contentType: false,
                processData: false,
                mode: 'same-origin',
                async: true,
                success : function(response)
                {
                    alert('Updated OK');
                    window.location.href = window.location.href;
                },
                error : function(xhr, status, error) {
                    alert(xhr.responseText);
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
                headers: {'X-CSRFToken': this.token,},
                contentType: false,
                processData: false,
                mode: 'same-origin',
                async: true,
                success : function(response)
                {
                    alert('Created OK');
                    window.location.href = window.location.href;
                },
                error : function(xhr, status, error) {
                    alert(xhr.responseText);
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
                error : function(xhr, status, error) {
                    alert(xhr.responseText);
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
                error : function(xhr, status, error) {
                    alert(xhr.responseText);
                }
            }
        )

        let model_json = model.responseJSON;
        let sorted_keys = Object.keys(model_json).sort();
        let sorted_values = sorted_keys.map(key => model_json[key]);

        return new this.model(...sorted_values)
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
        this.edit_form_id = String(repo.model.name) + "_form_edit";
        this.table_id = String(repo.model.name) + "_table";
        this.delete_link_name = String(repo.model.name) + "_delete_link";
        this.edit_link_name = String(repo.model.name) + "_edit_link";
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
    form(model = null){
        let form = document.createElement("form");
        if (model !== null){
            form.setAttribute('id', this.edit_form_id);
        }
        else{
            form.setAttribute('id', this.form_id);
        }


        Object.keys(this.repo.model.fields).sort().forEach(field_name=>{
            let field_type = this.repo.model.fields[field_name];

            let group = document.createElement("div");
            group.setAttribute('class', 'form-group');

            let span = document.createElement("span");
            span.textContent = field_name;

            let input = document.createElement("input");
            input.name = field_name;
            input.setAttribute('class', 'form-control');

            if (field_type === 'String'){
                input.setAttribute('type', 'text');
                if (model !== null) {
                    input.value = model[field_name];
                }
            }
            else if (field_type === 'Image'){
                input.setAttribute('type', 'file');
                // if (model !== null) {
                //     input.value = model[field_name];
                // }
            }
            else{
                input.setAttribute('type', 'text');
            }

            group.appendChild(span);
            group.appendChild(input);

            form.appendChild(group);
        })

        let button = document.createElement("button");
        button.setAttribute('type', 'submit');
        button.textContent = "submit";
        button.setAttribute("class", "submit");

        form.appendChild(document.createElement('br'));
        form.appendChild(button);

        return form
    }
    delete_link(model){
        let delete_link = document.createElement("a");
        delete_link.textContent = "❌";
        delete_link.style.color = "red";
        delete_link.style.cursor = 'pointer';
        delete_link.setAttribute('name', this.delete_link_name);
        delete_link.setAttribute('value', model[this.repo.model.pk_field]);

        return delete_link;
    }
    edit_link(model){
        let edit_link = document.createElement("a");
        edit_link.textContent = "✏️";
        edit_link.style.color = "orange";
        edit_link.style.cursor = "pointer";
        edit_link.setAttribute('name', this.edit_link_name);
        edit_link.setAttribute('value', model[this.repo.model.pk_field]);

        return edit_link
    }
    menu(model){
        let container = document.createElement("div");
        container.style.display = "flex";

        container.appendChild(this.delete_link(model));

        let divider = document.createElement("div");
        divider.style.width = "10px";
        container.appendChild(divider);

        container.appendChild(this.edit_link(model));

        return container;
    }
    table_row(model){
        // row
        let row = document.createElement("tr");

        // checkbox
        let td = document.createElement("td");
        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        td.appendChild(checkbox);
        row.appendChild(td);

        // menu
        td = document.createElement("td");

        td.appendChild(this.menu(model));
        row.appendChild(td);

        // content
        Object.keys(this.repo.model.fields).sort().forEach(field => {
            let field_type = this.repo.model.fields[field];

            let td = document.createElement("td");
            let value;

            if (field_type === 'String'){
                value = document.createElement("span");
                value.textContent = model[field];
            }
            else if(field_type === 'Image'){
                value = document.createElement("img");
                value.setAttribute('onclick', `window.location.href='${model[field]}'`)

                if (model[field]){
                    value.setAttribute('src', model[field]);
                }
                value.setAttribute('height', "50");
                value.setAttribute('width', "50");
            }
            else{
                value = document.createElement("span");
                value.textContent = model[field];
            }

            td.appendChild(value)
            row.appendChild(td);
        })

        return row;
    }
    table() {
        if (document.getElementById(this.table_id)) {
            document.getElementById(this.table_id).remove();
        }
        // table
        let table = document.createElement("table");
        table.setAttribute('id', this.table_id);
        table.setAttribute('class', 'table');

        let thead = table.createTHead();
        let headerRow = thead.insertRow();

        //checkbox
        let th = document.createElement("th");
        th.style.width = "5%";
        headerRow.appendChild(th);
        // action
        th = document.createElement("th");
        th.style.width = "5%";
        headerRow.appendChild(th);

        // header
        Object.keys(this.repo.model.fields).sort().forEach(field_name => {
            let th = document.createElement("th");
            th.textContent = field_name;
            headerRow.appendChild(th);
        })

        // body
        let tbody = table.createTBody();

        this.repo.collection.forEach((model) => {
            tbody.appendChild(this.table_row(model));
        });

        let tcaption = table.createCaption();
        tcaption.textContent = `Total: ${this.repo.collection.length} rows`;

        return table
    }
    modal(model){
        let modal_header = document.getElementById("entity_modal_header");
        let modal_body = document.getElementById("entity_modal_body");
        let modal_footer = document.getElementById("entity_modal_footer");

        modal_header.innerHTML = `<button type="button" class="close" aria-label="Close" onclick="$('#entity_modal').modal('hide')">
                                  <span aria-hidden="true">&times;</span>
                                  </button>`;

        modal_footer.innerHTML = `<button type="button" class="btn btn-secondary" onclick="$('#entity_modal').modal('hide')">Close</button>`;

        let header = document.createElement("span");
        header.textContent = String(this.repo.model.name) + " " + String(model[this.repo.model.pk_field]);

        modal_header.insertAdjacentElement('afterbegin', header);

        modal_body.insertAdjacentElement('afterbegin', this.form(model));

        $('#entity_modal').modal('show');
    }
}

/*
* @param {IView} view
* */
class IManager{
    constructor(view) {
        this.view = view;
    }
    listen_delete_links(){
        let self = this;
        let links = document.getElementsByName(this.view.delete_link_name);

        links.forEach(link =>{
            link.addEventListener('click', function(event){
                self.view.repo.delete(link.getAttribute('value'));
            })
        })
    }
    listen_edit_links(){
        let self = this;
        let links = document.getElementsByName(this.view.edit_link_name);

        links.forEach(link =>{
            link.addEventListener('click', function(event){
                self.view.modal(self.view.repo.retrieve(link.getAttribute('value')));
                self.listen_edit_form();
            })
        })
    }
    listen_form(){
        let self = this;
        $(`#${this.view.form_id}`).submit(function (event){
            event.preventDefault();
            self.view.repo.create(new FormData(this));
        })
        self.listen_delete_links();
        self.listen_edit_links();
    }
    listen_edit_form(){
        let self = this;
        $(`#${this.view.edit_form_id}`).submit(function (event){
            event.preventDefault();

            let form = new FormData(this);

            if ('file' in self.view.repo.model.fields){
                if (form.get('file').size === 0){
                    form.delete('file')
                }
            }

            self.view.repo.update(form.get(self.view.repo.model.pk_field), form);
        })
    }
}
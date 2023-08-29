const BRAND_URL = '/catalog/brands/';
const CSRF_TOKEN = $('input[name="csrfmiddlewaretoken"]').val();


class Brand extends IModel{
    static fields = ['name', 'slug', 'file'];
}

let repo = new IRepo(Brand, BRAND_URL, CSRF_TOKEN);
console.log(repo.list());

class BrandView{
    constructor() {
        this.selector_id = "brand_selector";
        this.form_id = "brand_form";
        this.fields = ["name", "slug", "file"];
    }
    // menu(brand_slug){
    //     let menu = document.createElement("div");
    //
    //     let delete_el = document.createElement("button");
    //     delete_el.innerText = "Удалить";
    //     delete_el.onclick = function(){delete_brand(brand_slug)};
    //
    //     let edit_el = document.createElement("button");
    //     edit_el.innerText = "Изменить";
    //
    //     let view_el = document.createElement('button');
    //     view_el.innerText = "Посмотреть"
    //
    //     let create_el = document.createElement("button");
    //     create_el.innerText = "Создать";
    //
    //     menu.insertAdjacentElement('beforeend', delete_el);
    //     menu.insertAdjacentElement('beforeend', edit_el);
    //     menu.insertAdjacentElement('beforeend', view_el);
    //     menu.insertAdjacentElement('beforeend', create_el);
    //
    //     return menu
    // }
    form(){
        let form = document.createElement('form');
        form.id = this.form_id;

        this.fields.forEach((field_name)=>{
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
    table_row(brand){
        let row = document.createElement("tr");

        let td = document.createElement("td");

        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";

        td.insertAdjacentElement("beforeend", checkbox);
        row.insertAdjacentElement('beforeend', td);

        this.fields.forEach((field)=>{
            let td = document.createElement("td");
            td.innerText = brand[field];
            row.insertAdjacentElement('beforeend', td);
        })

        return row;
    }
    table() {
        let table = document.createElement("table");

        table.setAttribute('class', 'table');
        table.style.color = "white";

        let table_head = document.createElement("thead");
        let table_head_row = document.createElement("tr");

        let td = document.createElement("td");
        table_head_row.insertAdjacentElement('beforeend', td);

        this.fields.forEach((field_name)=>{
            let td = document.createElement("td");
            td.innerText = field_name;
            table_head_row.insertAdjacentElement('beforeend', td);
        })

        table_head.insertAdjacentElement('beforeend', table_head_row);
        table.insertAdjacentElement('beforeend', table_head)

        let table_body = document.createElement("tbody");

        repo.list().forEach((brand)=>{
            table_body.insertAdjacentElement("beforeend", this.table_row(brand));
        });

        table.insertAdjacentElement('beforeend', table_body);

        return table
    }
    selector(){
        let select = document.createElement('select');
        select.id = this.selector_id;
        repo.list().forEach((brand)=>{
            let option = document.createElement('option');
            option.text = brand.name;
            option.value = brand.slug;
            select.insertAdjacentElement('beforeend', option);
        })
        return select
    }
}

document.getElementById('form_category').innerHTML = app.form()
document.getElementById('selector_form').innerHTML = app.selector()

// let view = new BrandView()
// document.write(view.form())
// document.write(view.selector().outerHTML)


let tree = document.getElementById('tree')
let refreshData = document.getElementById("refreshData")

function renderList(item, level = 0) {
    const listItem = document.createElement("li");
    const spanItem = document.createElement("span");
    spanItem.textContent = item.name;

    listItem.appendChild(spanItem);

    if (item.children && item.children.length > 0) {
        const sublist = document.createElement("ul");
        listItem.appendChild(sublist);
        for (const child of item.children) {
            const subListItem = renderList(child, level + 1);
            sublist.appendChild(subListItem);
        }
    }

    return listItem;
}

function get_categories() {
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax(
        {
            type: 'get',
            url: '/catalog/categories',
            headers: { 'X-CSRFToken': csrf_token },
            mode: 'same-origin',
            async: true,
            success: function (json) {
                data = JSON.parse(json)

                for (const item of data) {
                    const listItem = renderList(item);
                    tree.appendChild(listItem);
                }
                
                new TreeDragZone(tree);
                new TreeDropTarget(tree);
            },
            error: function (xhr, errmsg, err) {
                console.log(errmsg);
            }
        }
    )
}

refreshData.addEventListener('click', () => {
    refreshData.classList.toggle('transform');
    setTimeout(() => {
        tree.innerHTML = ""
        get_categories();
    }, 800)
    tree.innerHTML = ""
    get_categories();
})









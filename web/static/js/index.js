function filter_toggle(){
    let elements = document.getElementsByClassName('ant-menu-submenu-title');

    for (let i = 0; i < elements.length; i++){
        elements[i].addEventListener('click', function(event){
            let parent = this.parentNode;
            parent.classList.toggle('ant-menu-submenu-open');
            let child = parent.querySelector('ul');
            child.classList.toggle('ant-menu-hidden');
        })
    }
}

function filter_listen(){
    let form = document.getElementById("filter-form");
    let elements = document.querySelectorAll("#filter-form input");
    for (let i = 0; i < elements.length; i++){
        elements[i].addEventListener('change', function (event){
            form.submit();
        })
    }
}

$(function () {
    $("#search_q").autocomplete({
        source: "/catalog/products/autocomplete/",
        minLength: 2,
        delay: 100,
    });
});

$(document).ready(function(){
    $("a[href^='#']").on('click', function(event) {
        event.preventDefault();

        let target = this.hash;
        let $target = $(target);

        $('html, body').animate({
            'scrollTop': $target.offset().top
        }, 1000);
        console.log(1)
    });
});

$(document).ready(function(){
    let links = document.getElementsByName("page-link");

    let collapse_class = "ant-menu-overflow-item ant-menu-item ant-menu-item-selected ant-menu-item-only-child";
    let collapse_style = "opacity: 0; order: 0; height: 0px; overflow-y: hidden; pointer-events: none; position: absolute;";

    if (window.screen.width <= 900){
        for (let i = 0; i < links.length; i++){
            links[i].setAttribute('class', collapse_class);
            links[i].setAttribute('style', collapse_style);
        }
        document.getElementById('menu_links').insertAdjacentHTML('beforeend', `
            <li id="menu_links_list" class="ant-menu-overflow-item ant-menu-overflow-item-rest ant-menu-submenu ant-menu-submenu-horizontal ant-menu-submenu-selected" style="opacity: 1; order: -1; vertical-align: middle;" role="none">
                <div id="menu_links_div" role="menuitem" class="ant-menu-submenu-title" tabindex="-1" aria-expanded="false" aria-haspopup="true" style="vertical-align: middle; padding-top: 150%">
                    <span role="img" aria-label="ellipsis" class="anticon anticon-ellipsis">
                        <svg viewBox="64 64 896 896" focusable="false" data-icon="ellipsis" width="1em" height="1em" fill="currentColor" aria-hidden="true">
                            <path d="M176 511a56 56 0 10112 0 56 56 0 10-112 0zm280 0a56 56 0 10112 0 56 56 0 10-112 0zm280 0a56 56 0 10112 0 56 56 0 10-112 0z"></path>
                        </svg>
                    </span>
                <i class="ant-menu-submenu-arrow"></i>
            </div>
        </li>`)
    }

    if (window.screen.width <= 900){
        let filter_block = document.getElementById("filter-list-block");
        let products_block = document.getElementById("products-list-block");
        let new_filter_block = document.getElementById("new-filter-block");

        filter_block.remove();
        products_block.setAttribute('class', 'ant-col ant-col-24');

        filter_block.setAttribute('class', 'ant-col ant-col-24');
        new_filter_block.appendChild(filter_block);

        let elements = document.getElementsByClassName('ant-menu-submenu-title');
        for (let i = 0; i < elements.length; i++){
            let parent = elements[i].parentNode;
            let child = parent.querySelector('ul');
            if (child){
                parent.classList.toggle('ant-menu-submenu-open');
                child.classList.toggle('ant-menu-hidden');
            }
        }
    }
})

document.getElementById("menu_links").addEventListener('click', function(){
    if (document.getElementById("menu_links_list")) {
        let sticky_menu = document.getElementById("sticky_menu");
        sticky_menu.classList.toggle('more_info_hidden');
    }
})

function color_menu_links(){
    let links = document.getElementsByName("page-link");
    let path = window.location.href.split('/');
    path = path.filter(item => !(item === ''));

    if (path.length < 3){
        links[0].setAttribute('class', 'ant-menu-overflow-item ant-menu-item ant-menu-item-selected ant-menu-item-only-child');
        return
    }

    links.forEach(link=>{
        let a_el = link.children[0].children[0];
        let href = a_el.getAttribute('href');
        href = href.slice(1, href.length - 1);

        if (href === ""){
            return
        }

        if (path.includes(href)){
            link.setAttribute('class', 'ant-menu-overflow-item ant-menu-item ant-menu-item-selected ant-menu-item-only-child');
        }
        else{
            link.setAttribute('class', 'ant-menu-overflow-item ant-menu-item ant-menu-item-only-child')
        }
    })
}

function get_product(product_id){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    let data;
    $.ajax({
        type: 'get',
        url: '/catalog/products/' + String(product_id),
        headers: {'X-CSRFToken': csrf_token},
        mode: 'same-origin',
        async: false,
        success : function(json)
        {
            data = json;
        },
        error : function(xhr,errmsg,err) {
            alert('Повторите попытку позднее.');
        }
    })
    return data
}

function toggle_more_info(pk){
    document.getElementById(pk).classList.toggle('more_info_hidden');
}


// filter_listen();
color_menu_links();
filter_toggle();
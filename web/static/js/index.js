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
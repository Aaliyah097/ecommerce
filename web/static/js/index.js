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

// filter_listen();
filter_toggle();
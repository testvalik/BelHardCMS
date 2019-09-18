function add_1more_element(create_element, placeholder, post_name, append_to) {
    var item = document.createElement(create_element);
    item.placeholder = placeholder;
    item.className = "form-control m-sm-1";
    item.type = 'text';
    item.name = post_name;
    document.getElementById(append_to).appendChild(item);
}
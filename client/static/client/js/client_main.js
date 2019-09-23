function add_1more_element(create_element, placeholder, post_name, item_value, append_to) {
    var item = document.createElement(create_element);
    item.placeholder = placeholder;
    item.className = "form-control m-sm-1";
    item.type = 'text';
    item.name = post_name;
    item.value = item_value;
    document.getElementById(append_to).appendChild(item);
}

function add_more() {
            var origin = $("#origin_div").clone();
            var count = 0;
            $("#add_more").on("click", function () {
                var add = origin.clone();
                count += 1;
                console.log(count);

                add.attr("id", "new_div");
                add.appendTo("#div_to_add_new");
            });
        }
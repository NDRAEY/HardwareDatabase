var months = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря"
]

function switch_page() {
    var num = Number(document.getElementById("page_num_input").value) - 1
    var pagesize = Number(document.getElementById("records_in_page").value)

    if(num >= 0 && num < page_count) {
        urlParams.set('p', num);
    }

    if(pagesize >= 1 && pagesize <= 50) {
        urlParams.set('pagesize', pagesize);
    }

    location.href = `${window.location.pathname}?${urlParams.toString()}`
}

function delta_page(delta) {
    var num = Number(urlParams.get('p')) + delta

    urlParams.set('p', num);

    location.href = `${window.location.pathname}?${urlParams.toString()}`
}

function open_printable_ver() {
    location.href = `./print?${urlParams.toString()}`
}

function object_to_get(data) {
    var total = ""

    for(i of Object.keys(data)) {
        total += i + "=" + data[i] + "&"
    }

    return total
}

function send_add_form_data(data) {
    let resp = fetch("/cmd?" + object_to_get(data) + "cmd=new")
    let response = resp.then(response => {return response.json()})

    return response
}

function send_edit_form_data(old_data, data) {
    let resp = fetch("/cmd?" + object_to_get(old_data) + object_to_get(data) + "cmd=edit")
    let response = resp.then(response => {return response.json()})

    return response
}

function arrays_to_object(keys, values) {
    g = {}
    for(i in keys) {
        g[keys[i]] = values[i]
    }
    return g;
}

function delete_hw(inv_num) {
    dev = get_data_in_table(inv_num)
    console.log("GOT")
    really = confirm("Вы точно хотите удалить устройство: \"" + dev[2] + " " + dev[3] + " " + dev[4] + "\"?")

    if(really) {
        let resp = fetch("/cmd?inv_num=" + inv_num + "&cmd=del")
        resp.then(r => r.json()).then(j => {
            if(j.ok)
                location.reload()
        })
    }
}

function get_data_in_table(inv_num) {
    row = document.getElementById(String(inv_num)).childNodes.entries()
    
    cols = Array.from(row).map(a => a[1]).filter(a => a.tagName == "TD").map(a => a.innerHTML) 

    cols = cols.slice(0, cols.length - 1)

    return cols
}

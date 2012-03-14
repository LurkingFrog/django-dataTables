function load_data_table(table_id, table_type, csrf) {
    $.ajax({
	type: 'POST',
	url: "datatables/ajax_get_records/",
        data: {
	    csrfmiddlewaretoken: csrf,
	    table_type: table_type
        },
	success:  function(resp){
	    resp["bProcessing"] = true;
	    $("#" + table_id).dataTable(resp);
	    var col_count = resp['aoColumns'].length;
	    build_buttons(resp['buttons'], table_id, col_count);
        },
	error: function(xhr, textStatus, errorThrown) {
	    alert("There was a 500 error: " + textStatus + ":" + errorThrown);
	},
	dataType: "json",
    });
};


function build_buttons(buttons, table_id, col_count) {
    target = $("#" + table_id + "_footer");
    target.attr('colspan', col_count);

    target.html("");
    for (x in buttons) {
	var button = buttons[x];
	new_item = $('<button/>', {
	    text: button['label'],   
	});
	new_item.click(
	    function(e) {
		e.preventDefault();
		button_click(
		    button['action'],
		    button['target'],
		    target.parents("form")
		);
	    }
	)
	target.append(new_item);
    }
}


function button_click(action, target, form){
    if (action == "JUMP") {
	form.attr('action', target);
	form.submit();
    }
    
}


function load_script(filename) {
    var script = document.createElement('script');
    script.setAttribute("type","text/javascript");
    script.setAttribute("src", filename);
    document.getElementsByTagName("head")[0].appendChild(script);
}


function wait_ready() {
    // Continually polls to see if jQuery is loaded.
    var time_elapsed = 0
    while (time_elapsed <= 5000) { // and we havn't given up trying...
	if (typeof $ == "undefined") { // if jQuery isn't loaded yet...
	    sleep(200);
	    time_elapsed = time_elapsed + 200
	} else {
	    time_elapsed = 5001;
	}
    }
}


function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
}


function load_required_scripts(path) {
    // TODO: make the sources able to be overidden
    // We check if jquery is installed and add it if not
    if (typeof $ === 'undefined') {
	load_script(path + "datatables/js/jquery.js");
	wait_ready();

	// This is a bug that I will figure out later, since it is possible
	// to have already loaded jquery
	load_script(path + "datatables/js/jquery.dataTables.min.js");
//	wait_ready();
    }
}
$(document).ready( function () {
	function draw(data) {
		if ( $.fn.dataTable.isDataTable( '#table-container' ) ) {
			var table = $("#table-container").DataTable()
			table.clear().rows.add(data.data).draw();
		} else {
			$('#loader').hide()
			$('#table-container').empty().dataTable({
				data: data['data'], 
				columns: data['columns'],
				retrieve: true,
			})
		}
		return tbody
	}
	async function get_data() {
	    const tbody = ''
		const response = await fetch('/kraken');
	    const reader = response.body.getReader();
	    

		while (true) {
			const { value, done } = await reader.read();
			if (done) break;
			try {
			    let result = new TextDecoder("utf-8").decode(value);
				let data = JSON.parse(result);
				for (channelID in data) {
					let temp = {
						'data': [],
						'columns': []
					}
					for (pair in data) {
						temp.data.push(data[pair])
						if (temp.columns.length <= 0) {
							p = Object.keys(data[pair])
							for (name in p) {										
								temp.columns.push({'title': p[name], 'data': p[name]})
							}
						}
					}
					tbody = draw(temp)
				}
		    } catch(e) {
		    }
		}
	}
	get_data()
})
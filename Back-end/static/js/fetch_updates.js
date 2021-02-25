$(document).ready( function () {
	let tickers_count = parseInt($('#tickers_count').val())
	function draw(data) {
		if ( $.fn.dataTable.isDataTable( '#table-container' ) ) {
			var table = $("#table-container").DataTable()
			table.clear().rows.add(data.data).draw(false);
			console.log(tickers_count)
			if (table.rows().count() >= tickers_count)  {
				$('loader_table').fadeOut('400')
			}
			else {
				$('#table-container_info').append('<img id="loader_table" src="/static/img/loader.gif">')
			}
		} else {
			$('.main-header').hide()
			$('#table-container').empty().dataTable({
				data: data['data'], 
				columns: data['columns'],
				retrieve: true,
			})
			$('#table-container_info').append('<img id="loader_table" src="/static/img/loader.gif">')
		}
	}

	async function get_data() {
	    const response = await fetch('/monitoring_stream');
	    const reader = response.body
		.getReader()
	    let ticker_store = {}
            let decoder = new TextDecoder("utf-8")

		while (true) {
			const { value, done } = await reader.read();
			if (done) break;
			let err_value = ''
			try {
			    let result = decoder.decode(value);
				result = result.split('-next-')[1];
				let data = JSON.parse(result);
				binance_data = data.binance
				kraken_data = data.kraken
				let temp = {
					'data': [],
					'columns': []
				}
				for (stock in data) {
					for (const [pair, price] of Object.entries(data[stock])) {
					    // console.log(ticker_store);
						if (ticker_store.hasOwnProperty(pair)) {
							if (stock === 'binance') {
								ticker_store[pair][1] = price
							} else if (stock === 'kraken') {
								ticker_store[pair][2] = price
							}
						} else {
							if (stock === 'binance') {
								ticker_store[pair] = [pair, price, '-']
							} else if (stock === 'kraken') {
								ticker_store[pair] = [pair, '-', price]
							}
						}
					}
				}
				temp.data = Object.values(ticker_store)
				//console.log(temp.data)
				temp.columns = [
					{
						'title': 'pair',
					},
					{
						'title': '<img class="columns_logo" src="/static/img/binance_logo.svg" alt="binance"/>',
					},
					{
						'title': '<img class="columns_logo" src="/static/img/kraken_logo.png" alt="kraken"/>',
					},
				]
				draw(temp)
		    } catch(e) {
			//console.log(e)
			}
		}
	}
	get_data()
})

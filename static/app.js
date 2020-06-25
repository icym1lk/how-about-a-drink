const $drinkImage = $('#drink-image');

$('#query_type').change(function() {
	$('#query').attr('placeholder', $(this).find(':selected').data('name'));
});

$drinkImage.on('click', function(e) {
	let $drinkID = $(this).data('drink-id');
	callAPI($drinkID);
});

async function callAPI(id) {
	const res = await axios({
		method: 'get',
		url: `https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=${id}`
	})
		.then((res) => {
			console.log('success');
			console.log(res);
			// handleResponseSuccess(res.data);
		})
		.catch((err) => {
			console.log('fail');
			console.log(err.response);
			// handleResponseFail(err.response.data);
		});
}

const $drinkImage = $('#drink-image');

$('#query_type').change(function() {
	$('#query').attr('placeholder', $(this).find(':selected').data('name'));
});

$drinkImage.on('click', function(e) {
	let $drinkID = $(this).data('drink-id');
});

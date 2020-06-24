$('#query_type').change(function() {
	$('#query').attr('placeholder', $(this).find(':selected').data('name'));
});

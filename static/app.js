const $body = $('body');
const $drinkImage = $('#drink-image');

$('#query_type').change(function() {
	$('#query').attr('placeholder', $(this).find(':selected').data('name'));
});

$drinkImage.on('click', function(e) {
	let $drinkID = $(this).data('drink-id');
	callAPI($drinkID);
});

// deal with successful response from our lucky-num API
function handleResponseSuccess(resp) {
	// console.log(resp);
	let name = resp[0].strDrink;
	let category = resp[0].strCategory;
	let IBA = resp[0].strIBA ? resp[0].strIBA : 'Not Applicable';
	let alcohol = resp[0].strAlcoholic;

	if (alcohol === 'Alcoholic') {
		alcohol = 'Yes';
	} else if (alcohol === 'Optional Alcohol') {
		alcohol = 'Optional Alcohol';
	} else {
		alcohol = 'No';
	}

	$body.append(`
		<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  			<div class="modal-dialog">
    			<div class="modal-content">
      				<div class="modal-header">
        				<h5 class="modal-title" id="exampleModalLabel">${name}</h5>
        				<button type="button" class="close" data-dismiss="modal" aria-label="Close">
          					<span aria-hidden="true">&times;</span>
        				</button>
      				</div>
      				<div class="modal-body">
						<ul>
							<li>
								Category: ${category}
							</li>
							<li>
								IBA: ${IBA}
							</li>
							<li>
								Alcoholic: ${alcohol}
							</li>
						</ul>
						<p>${resp[0].strInstructions}</p>
      				</div>
      				<div class="modal-footer">
        				<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        				<button type="button" class="btn btn-primary">Save changes</button>
      				</div>
    			</div>
  			</div>
		</div>
	`);
}

// call TheCocktailDB API to retrieve drink details based on id passed in
async function callAPI(id) {
	const res = await axios({
		method: 'get',
		url: `https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=${id}`
	})
		.then((res) => {
			// console.log(res.data.drinks);
			resp = res.data.drinks;
			handleResponseSuccess(resp);
		})
		.catch((err) => {
			console.log(err.response);
			// handleResponseFail(err.response.data);
		});
}

$(async function() {
	// cache some selectors
	const $body = $('body');

	// change search bar placeholder text depending on dropdown selection
	$('#query_type').change(function() {
		$('#query').attr('placeholder', $(this).find(':selected').data('name'));
	});

	// get drinkID from data attr on imgs
	$body.on('click', '#drink-image', function(e) {
		// console.log(e.target);
		let $drinkID = $(this).data('drink-id');
		// console.log($drinkID);
		callAPI($drinkID);
	});

	// $('#drink-image').on('click', function() {

	// 	});
	// });

	// $('#drink-modal').on('hidden.bs.modal', function(e) {
	// 	console.log('modal hidden');
	// 	$('.modal-content').html('');
	// });

	// deal with successful response from our lucky-num API
	function filterAPIResData(res) {
		// console.log(resp);
		const name = res[0].strDrink;
		const category = res[0].strCategory;
		const IBA = res[0].strIBA ? res[0].strIBA : 'No Designation';
		let alcohol = res[0].strAlcoholic;
		const instructions = res[0].strInstructions;

		if (alcohol === 'Alcoholic') {
			alcohol = 'Yes';
		} else if (alcohol === 'Optional Alcohol') {
			alcohol = 'Optional Alcohol';
		} else {
			alcohol = 'No';
		}
		// console.log(name, category, IBA, alcohol);
		createDrinkModal(name, category, IBA, alcohol, instructions);
	}

	// create HTML for drink modal
	function createDrinkModal(name, category, IBA, alcohol, instructions) {
		const drinkInfo = `
			<div class="modal fade" id="drink-modal" tabindex="-1" role="dialog" aria-labelledby="drinkModalLabel" aria-hidden="true">
				<div class="modal-dialog modal-dialog-centered">
					<div class="modal-content">
						<div class="modal-header">
							<h5 class="modal-title" id="drinkModalLabel">${name}</h5>
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
									International Bartenders Association: ${IBA}
								</li>
								<li>
									Alcoholic: ${alcohol}
								</li>
							</ul>
							<p>${instructions}</p>
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
							<button type="button" class="btn btn-primary">Save changes</button>
						</div>
					</div>
				</div>
			</div>
		`;
		$body.append(drinkInfo);
	}

	// call TheCocktailDB API to retrieve drink details based on id passed in
	async function callAPI(id) {
		const res = await axios({
			method: 'get',
			url: `https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=${id}`
		})
			.then((res) => {
				// console.log(res.data.drinks);
				res = res.data.drinks;
				filterAPIResData(res);
			})
			.catch((err) => {
				console.log(err);
				// handleResponseFail(err.response.data);
			});
	}
});

$(async function() {
	// change search bar placeholder text depending on dropdown selection
	$('#query_type').change(function() {
		$('#query').attr('placeholder', $(this).find(':selected').data('name'));
	});

	// get drinkID from data attr on imgs
	$('.card').on('click', '#drink-image', function(e) {
		// console.log(e.target);
		let $drinkID = $(this).data('drink-id');
		// console.log($drinkID);
		callAPI($drinkID);
	});

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

	// deal with successful response from our lucky-num API
	function filterAPIResData(res) {
		// console.log(resp);
		const id = res[0].idDrink;
		const name = res[0].strDrink;
		const category = res[0].strCategory;
		const IBA = res[0].strIBA ? res[0].strIBA : 'No Designation';
		let alcohol = res[0].strAlcoholic;
		const instructions = res[0].strInstructions;
		const ingredients = {
			[res[0].strIngredient1]: res[0].strMeasure1,
			[res[0].strIngredient2]: res[0].strMeasure2,
			[res[0].strIngredient3]: res[0].strMeasure3,
			[res[0].strIngredient4]: res[0].strMeasure4,
			[res[0].strIngredient5]: res[0].strMeasure5,
			[res[0].strIngredient6]: res[0].strMeasure6,
			[res[0].strIngredient7]: res[0].strMeasure7,
			[res[0].strIngredient8]: res[0].strMeasure8,
			[res[0].strIngredient9]: res[0].strMeasure9,
			[res[0].strIngredient10]: res[0].strMeasure10,
			[res[0].strIngredient11]: res[0].strMeasure11,
			[res[0].strIngredient12]: res[0].strMeasure12,
			[res[0].strIngredient13]: res[0].strMeasure13,
			[res[0].strIngredient14]: res[0].strMeasure14,
			[res[0].strIngredient15]: res[0].strMeasure15
		};

		if (alcohol === 'Alcoholic') {
			alcohol = 'Yes';
		} else if (alcohol === 'Optional Alcohol') {
			alcohol = 'Optional Alcohol';
		} else {
			alcohol = 'No';
		}
		// console.log(name, category, IBA, alcohol);
		createDrinkModal(id, name, category, IBA, alcohol, instructions, ingredients);
	}

	function filterIngredients(ingredients) {
		for (let k in ingredients) {
			if (k !== 'null') {
				const $newLI = k + ' > ' + ingredients[k];
				createIngredientLI($newLI);
			}
		}
	}

	function createIngredientLI(ingredient) {
		const $li = $(`
			<li>${ingredient}</li>
		`);
		$('.modal-body > ul > li > ul').append($li);
	}

	// create HTML for drink modal
	async function createDrinkModal(id, name, category, IBA, alcohol, instructions, ingredients) {
		const drinkInfo = `
			<div class="modal fade" id="drink-modal-${id}" tabindex="-1" role="dialog" aria-labelledby="drinkModalLabel" aria-hidden="true">
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
								<li>
									Ingredients:
									<ul>
										${filterIngredients(ingredients)}
									</ul>
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
		$('body').append(drinkInfo);
	}
});

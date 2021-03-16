// const API_ID = '7ad5f5c3';
// const API_KEY = '75d853b05cbe14a1b05b4fd0c1f472bc';
// const BASE_URL = 'https://api.edamam.com/search?';
let frm = 0;
let to = 8;

// const $searchForm = $('#searchbar');
// const $searchResults = $('#search-results');
// $searchForm.on('submit', async function(e) {
// 	e.preventDefault();
// 	let searchterm = $('#search-input').val();

// 	res = await axios.get(`${BASE_URL}q=${searchterm}&app_id=${API_ID}&app_key=${API_KEY}&from=${from}&to=${to}`);

// 	let recipes_arr = res.data.hits;
// 	$('.res-cols').remove();

// 	renderResults(recipes_arr);
// 	$('.more-btn').toggleClass('hidden');
// 	$('.more-btn').on('click', async function(e) {
// 		e.preventDefault();
// 		console.log('more clicked');
// 		searchterm = res.data.q;
// 		from += 9;
// 		to += 9;
// 		res = await axios.get(`${BASE_URL}q=${searchterm}&app_id=${API_ID}&app_key=${API_KEY}&from=${from}&to=${to}`);

// 		recipes_arr = res.data.hits;
// 		renderResults(recipes_arr);
// 	});
// });

// function renderResults(recipes_arr) {
// 	for (r of recipes_arr) {
// 		if ($('#curr_user').val() === 'None') {
// 			$searchResults.append(`<div class="col-3 res-cols">
//                                 <div class="card">
//                                 <a href="${r.recipe.url}" class="d-flex justify-content-center">
//                                 <img class="result-img card-img-top img-fluid" src="${r.recipe.image}" alt="${r.recipe
// 				.label} photo">
//                                 </a>
//                                 <div class="container-fluid p-0">
//                                 <div class="card-body container-fluid">
//                                 <h5 class="card-title text-light my-1 mr-0 w-100">${r.recipe.label}</h5>
//                                 <p class="card-text text-light cuisine-type">${r.recipe.cuisineType === undefined
// 									? 'world'
// 									: r.recipe.cuisineType}</p>
//                                 <a href="${r.recipe.url}" class="btn btn-sm text-light recipe-btn mb-2">View Recipe</a>
//                                 </div>
//                                 </div>
//                                 </div>
//                                </div>`);
// 		} else {
// 			$searchResults.append(`<div class="col-3 res-cols">
//                                 <div class="card">
//                                 <a href="${r.recipe.url}" class="d-flex justify-content-center">
//                                 <img class="result-img card-img-top img-fluid" src="${r.recipe.image}" alt="${r.recipe
// 				.label} photo">
//                                 </a>
//                                 <div class="container-fluid p-0">
//                                 <div class="card-body container-fluid">
//                                 <h5 class="card-title text-light my-1 mr-0 w-100">${r.recipe.label}</h5>
//                                 <p class="card-text text-light cuisine-type">${r.recipe.cuisineType === undefined
// 									? 'world'
// 									: r.recipe.cuisineType}</p>
//                                 <a href="${r.recipe.url}" class="btn btn-sm text-light recipe-btn mb-2">View Recipe</a>
//                                 <form method="POST" action="/favorites/add">
//                                 <input class="add-favorite-input" name="add-favorite-input" value="${r.recipe
// 									.uri}" hidden>

//                                 <button href="" class="btn btn-sm text-light save-recipe-btn" type="submit">Save Recipe</button>
//                                 </form>
//                                 </div>
//                                 </div>
//                                 </div>
//                                </div>`);
// 		}
// 	}
// 	$searchResults.append(`<div class="hidden" style="height: 40px"></div>`);
// }

// async function checkIfSaved(recipe_uri) {
// 	return await axios.get('/check_saved');
// 	// should return boolean after checking if recipe_uri is in res.data.uris
// 	return res.data.uris.indexOf(recipe_uri) !== -1;
// }

// ########################################################################################################

const $searchForm = $('.searchbar');
const $searchResults = $('#search-results');
$searchForm.on('submit', async function(e) {
	e.preventDefault();
	let searchterm = $('#search-input').val();

	let res = await axios.get('/search_api', { params: { searchterm, frm, to } });

	// console.log(SavedRecipes);
	$('.res-cols').remove();

	renderResults(res.data);

	$('.more-btn').toggleClass('hidden');
	$('.more-btn').on('click', async function(e) {
		e.preventDefault();
		console.log('more clicked');

		frm += 9;
		to += 9;
		res = await axios.get('/search_api', { params: { searchterm, frm, to } });

		renderResults(res.data);
	});
});

async function renderResults(recipes_arr) {
	for (r of recipes_arr) {
		if ($('#curr_user').val() === 'None') {
			$searchResults.append(`<div class="col-3 res-cols">
	                                <div class="card">
	                                <a href="${r.recipe.url}" class="d-flex justify-content-center">
	                                <img class="result-img card-img-top img-fluid" src="${r.recipe.image}" alt="${r.recipe
				.label} photo">
	                                </a>
	                                <div class="container-fluid p-0">
	                                <div class="card-body container-fluid">
	                                <h5 class="card-title text-light my-1 mr-0 w-100">${r.recipe.label}</h5>
	                                <p class="card-text text-light cuisine-type">${r.recipe.cuisineType === undefined
										? 'world'
										: r.recipe.cuisineType}</p>
	                                <a href="${r.recipe.url}" class="btn btn-sm text-light recipe-btn mb-2">View Recipe</a>
	                                </div>
	                                </div>
	                                </div>
	                               </div>`);
		} else {
			let resp = await axios.get('/get_favorites_uri');
			let SavedRecipes = resp.data.uris;
			// check if r.recipe.uri in USER_FAVORITES
			if (SavedRecipes.includes(r.recipe.uri) === false) {
				$searchResults.append(`<div class="col-3 res-cols">
				<div class="card">
				<a href="${r.recipe.url}" class="d-flex justify-content-center">
				<img class="result-img card-img-top img-fluid" src="${r.recipe.image}" alt="${r.recipe.label} photo">
				</a>
				<div class="container-fluid p-0">
				<div class="card-body container-fluid">
				<h5 class="card-title text-light my-1 mr-0 w-100">${r.recipe.label}</h5>
				<p class="card-text text-light cuisine-type">${r.recipe.cuisineType === undefined
					? 'world'
					: r.recipe.cuisineType}</p>
				<a href="${r.recipe.url}" class="btn btn-sm text-light recipe-btn mb-2">View Recipe</a>
				<form method="POST" action="/favorites/add">
				<input class="add-favorite-input" name="add-favorite-input" value="${r.recipe.uri}" hidden>

				<button href="" class="btn btn-sm text-light save-recipe-btn" type="submit">Save Recipe</button>
				</form>
				</div>
				</div>
				</div>
			   </div>`);
			} else {
				$searchResults.append(`<div class="col-3 res-cols">
				<div class="card">
				<a href="${r.recipe.url}" class="d-flex justify-content-center">
				<img class="result-img card-img-top img-fluid" src="${r.recipe.image}" alt="${r.recipe.label} photo">
				</a>
				<div class="container-fluid p-0">
				<div class="card-body container-fluid">
				<h5 class="card-title text-light my-1 mr-0 w-100">${r.recipe.label}</h5>
				<p class="card-text text-light cuisine-type">${r.recipe.cuisineType === undefined
					? 'world'
					: r.recipe.cuisineType}</p>
				<a href="${r.recipe.url}" class="btn btn-sm text-light recipe-btn mb-2">View Recipe</a>
				<a href="/favorites" class="text-center d-flex justify-content-center favorited-text py-0">Favorite <i class="fab fa-pagelines"></i></a>
				</div>
				</div>
				</div>
			   </div>`);
			}
		}
	}
	$searchResults.append(`<div class="hidden" style="height: 40px"></div>`);
}

$('#favorites-search-form').on('keyup', async function(e) {
	e.preventDefault();
	const searchterm = $('#favorites-search-input').val();

	if (searchterm === '') {
		res = await axios.get('/get_favorites');
		console.log(res);
		$('#favorites').empty();

		for (r of res.data) {
			$('#favorites').append(renderFavorite(r));
		}

		$('#favorites-search-form').trigger('reset');
	} else {
		res = await axios.get(`get_favorites/${searchterm}`);
		$('#favorites').empty();

		for (r of res.data) {
			$('#favorites').append(renderFavorite(r));
		}

		// $('#favorites-search-form').trigger('reset');
	}
});

function renderFavorite(favRecipe) {
	return $(`<div class="col-3 res-cols">
	<div class="card fav-card">
	<a href="${favRecipe.url}" class="d-flex justify-content-center">
	<img class="result-img card-img-top img-fluid" src="${favRecipe.image_url}" alt="${favRecipe.name} photo">
	</a>
	<div class="container-fluid px-0">
	<div class="card-body mt-0">
	<h5 class="card-title text-light">${favRecipe.name}</h5>
	<p class="card-text text-light cuisine-type">${favRecipe.cuisine_type}</p>
	<a href="${favRecipe.url}" class="btn btn-sm text-light recipe-btn mb-2">View Recipe</a>
	<form action="/favorites/remove" method="POST">
		<input class="delete-favorite-input" name="remove-favorite-input" value="${favRecipe.uri}" hidden>
		<button class="btn btn-sm text-light remove-btn mb-2" type="submit">Remove Recipe <i class="fas fa-trash"></i></button>
	</form>
	
	</div>
	</div>
   </div>
</div>`);
}

$('#own-search-form').on('keyup', async function(e) {
	e.preventDefault();
	const searchterm = $('#own-search-input').val();

	if (searchterm === '') {
		res = await axios.get('/get_own');
		console.log(res);
		$('#own-recipes').empty();

		for (r of res.data) {
			$('#own-recipes').append(renderOwn(r));
		}

		$('#own-search-form').trigger('reset');
	} else {
		res = await axios.get(`get_own/${searchterm}`);
		$('#own-recipes').empty();

		for (r of res.data) {
			$('#own-recipes').append(renderOwn(r));
		}

		// $('#favorites-search-form').trigger('reset');
	}
});

function renderOwn(ownRecipe) {
	return $(`<div class="col-3 res-cols">
	<div class="card fav-card">
	<a href="${ownRecipe.url}" class="d-flex justify-content-center">
	<img class="result-img card-img-top img-fluid" src="${ownRecipe.image_url}" alt="${ownRecipe.name} photo">
	</a>
	<div class="container-fluid px-0">
	<div class="card-body mt-0">
	<h5 class="card-title text-light">${ownRecipe.name}</h5>
	<p class="card-text text-light cuisine-type">${ownRecipe.cuisine_type}</p>
	<a href="${ownRecipe.url}" class="btn btn-sm text-light recipe-btn mb-2">View Recipe</a>
	<form action="/favorites/remove" method="POST">
		<input class="delete-favorite-input" name="remove-favorite-input" value="${ownRecipe.uri}" hidden>
		<button class="btn btn-sm text-light remove-btn mb-2" type="submit">Remove Recipe <i class="fas fa-trash"></i></button>
	</form>
	
	</div>
	</div>
   </div>
</div>`);
}

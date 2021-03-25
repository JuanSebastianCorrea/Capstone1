let frm;
let to;
let searchterm;
const $searchForm = $('.searchbar');
const $searchResults = $('#search-results');
const $searchInput = $('#search-input');

$('.more-btn').hide();

$searchInput.on('focus', () => {
	$searchInput.val('');
});

$searchForm.on('submit', async function(e) {
	e.preventDefault();
	$('.res-cols').remove();
	$('.hidden').remove();
	frm = 0;
	to = 8;
	searchterm = $searchInput.val();

	let res = await axios.get('/search_api', { params: { searchterm, frm, to } });

	renderResults(res.data);

	$('.more-btn').show();
});

$('.more-btn').on('click', async function(e) {
	e.preventDefault();
	console.log('more clicked');
	console.log($searchInput.val());

	frm += 9;
	to += 9;
	console.log(frm);
	console.log(to);
	console.log(searchterm);
	res = await axios.get('/search_api', { params: { searchterm, frm, to } });

	renderResults(res.data);
});

async function renderResults(recipes_arr) {
	for (r of recipes_arr) {
		console.log(r);
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
			// let resp = await axios.get('/get_favorites_uri');
			// let SavedRecipes = resp.data.uris;
			// check if r.recipe.uri in USER_FAVORITES to mark it accordingly
			if (r.bookmarked === false) {
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

$('.wrapper').on('scroll', () => {
	$('.scroll-sign').detach();
});

setTimeout(() => {
	$('.scroll-sign').fadeOut();
}, 4000);

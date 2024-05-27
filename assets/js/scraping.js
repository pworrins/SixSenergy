// Load data from JSON file
fetch('A6Scrapy4.json')
  .then(response => response.json())
  .then(data => {
    // Sort data by rank (assuming the 'rank' property exists)
    data.sort((a, b) => a.rank - b.rank);
    renderMangaList(data);

    document.getElementById('sort-title').addEventListener('click', sortByTitle);
    document.getElementById('sort-rank').addEventListener('click', sortByRank);

    function sortByTitle() {
      data.sort((a, b) => a.title.localeCompare(b.title));
      renderMangaList(data);
    }

    function sortByRank() {
      data.sort((a, b) => a.rank - b.rank);
      renderMangaList(data);
    }

    function renderMangaList(data) {
      const mangaList = document.getElementById('manga-list');
      mangaList.innerHTML = ''; // Clear the existing content

      data.forEach(manga => {
        const cardHTML = `
          <div class="col-md-6 mb-4">
            <div class="card h-100 shadow border-0">
              <!-- Change img tag to link for lightbox -->
              <a href="${manga.image_url}" data-lightbox="manga" data-title="${manga.title} cover">
                <img src="${manga.image_url}" class="dish-img" alt="${manga.title} cover">
              </a>
              <div class="card-content">
                <h5 class="card-title">${manga.title}</h5>
                <p class="card-text">${manga.synopsis.substring(0, 200)}...</p>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item"><strong>Rank:</strong> ${manga.rank}</li>
                  <li class="list-group-item"><strong>Rating:</strong> ${manga.rating}</li>
                  <li class="list-group-item"><strong>Genres:</strong> ${manga.genres.join(', ')}</li>
                  <li class="list-group-item"><strong>Publish:</strong> ${manga.publish}</li>
                  <li class="list-group-item"><strong>Authors:</strong> ${manga.authors.join(', ')}</li>
                  <li class="list-group-item"><strong>Characters:</strong> ${manga.characters.join(', ')}</li>
                  <li class="list-group-item"><strong>Status:</strong> ${manga.status}</li>
                  <li class="list-group-item"><strong>Popularity:</strong> ${manga.popularity}</li>
                </ul>
                <div class="card-footer bg-transparent border-0">
                  <a href="${manga.url}" class="btn btn-primary btn-sm" target="_blank">More info</a>
                </div>
              </div>
            </div>
          </div>
        `;

        mangaList.innerHTML += cardHTML;
      });
    }
  });
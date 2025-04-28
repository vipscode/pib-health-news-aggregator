document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const articlesList = document.getElementById('articles-list');
    const articleContent = document.getElementById('article-content');
    const articlesCount = document.getElementById('articles-count');
    const categoryFilter = document.getElementById('category-filter');
    const searchInput = document.getElementById('search-input');
    const updateButton = document.getElementById('update-button');
    const lastUpdated = document.getElementById('last-updated');
    
    // Articles data
    let articles = [];
    let selectedArticleId = null;

    // Load articles data
    async function loadArticles() {
        try {
            const response = await fetch('data/articles.json');
            articles = await response.json();
            
            // Update last updated date
            if (articles.length > 0) {
                lastUpdated.textContent = new Date().toLocaleDateString();
            }
            
            filterAndDisplayArticles();
        } catch (error) {
            console.error('Error loading articles:', error);
            articlesList.innerHTML = '<p>Error loading articles. Please try again later.</p>';
        }
    }

    // Filter and display articles
    function filterAndDisplayArticles() {
        const category = categoryFilter.value;
        const searchQuery = searchInput.value.toLowerCase();
        
        let filteredArticles = [...articles];
        
        // Apply category filter
        if (category !== 'All') {
            filteredArticles = filteredArticles.filter(article => article.category === category);
        }
        
        // Apply search filter
        if (searchQuery) {
            filteredArticles = filteredArticles.filter(article => 
                article.title.toLowerCase().includes(searchQuery) || 
                article.content.toLowerCase().includes(searchQuery)
            );
        }
        
        // Sort by date (newest first)
        filteredArticles.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        // Update count
        articlesCount.textContent = `Recent Press Releases (${filteredArticles.length})`;
        
        // Render articles
        renderArticlesList(filteredArticles);
    }

    // Render articles list
    function renderArticlesList(filteredArticles) {
        if (filteredArticles.length === 0) {
            articlesList.innerHTML = '<p>No articles found matching your criteria</p>';
            return;
        }
        
        let html = '';
        filteredArticles.forEach(article => {
            const isSelected = article.id === selectedArticleId;
            html += `
                <div class="article-card ${isSelected ? 'selected' : ''}" data-id="${article.id}">
                    <div class="article-header">
                        <h3 class="article-title">${article.title}</h3>
                        <span class="article-category">${article.category}</span>
                    </div>
                    <p class="article-summary">${article.summary}</p>
                    <p class="article-date">${article.date}</p>
                </div>
            `;
        });
        
        articlesList.innerHTML = html;
        
        // Add click event listeners
        document.querySelectorAll('.article-card').forEach(card => {
            card.addEventListener('click', function() {
                const id = parseInt(this.getAttribute('data-id'));
                selectArticle(id);
            });
        });
        
        // If we have a selected article and it's not in the filtered list, clear selection
        if (selectedArticleId !== null) {
            const articleStillExists = filteredArticles.some(article => article.id === selectedArticleId);
            if (!articleStillExists) {
                selectedArticleId = null;
                showPlaceholder();
            }
        }
    }

    // Select an article
    function selectArticle(id) {
        selectedArticleId = id;
        
        // Remove selected class from all cards
        document.querySelectorAll('.article-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Add selected class to current card
        const selectedCard = document.querySelector(`.article-card[data-id="${id}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
        
        // Find the article
        const article = articles.find(article => article.id === id);
        
        // Display article content
        if (article) {
            articleContent.innerHTML = `
                <span class="detail-category">${article.category}</span>
                <p class="detail-date">${article.date}</p>
                <h2 class="detail-title">${article.title}</h2>
                <div class="detail-content">
                    <p>${article.content}</p>
                </div>
                <a href="${article.url}" class="original-link" target="_blank">View original press release</a>
            `;
        }
    }

    // Show placeholder
    function showPlaceholder() {
        articleContent.innerHTML = `
            <div class="placeholder-message">
                <p>Select an article to view details</p>
            </div>
        `;
    }

    // Event listeners
    categoryFilter.addEventListener('change', filterAndDisplayArticles);
    searchInput.addEventListener('input', filterAndDisplayArticles);
    
    // Mock update button (in a real application, this would trigger the scraper)
    updateButton.addEventListener('click', function() {
        alert('In a real implementation, this would trigger the scraper to fetch new articles.');
    });

    // Initial load
    loadArticles();
});

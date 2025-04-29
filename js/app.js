document.addEventListener("DOMContentLoaded", function () {
  const dataUrl = "assets/data/categorized_data.json";
  const categorySelect = document.getElementById("categorySelect");
  const newsContainer = document.getElementById("newsContainer");

  let allArticles = [];

  // Categories to filter
  const categories = [
    "All",
    "Digital Health",
    "Medical Technologies",
    "Pharmaceuticals",
    "Climate Change and Health",
    "AMR",
    "Others"
  ];

  // Populate dropdown
  categories.forEach(category => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    categorySelect.appendChild(option);
  });

  // Fetch data
  fetch(dataUrl)
    .then(response => response.json())
    .then(data => {
      allArticles = data;
      renderArticles(allArticles);
    })
    .catch(error => {
      console.error("Error loading JSON:", error);
      newsContainer.innerHTML = "<p>Failed to load news data.</p>";
    });

  // Render articles
  function renderArticles(articles) {
    newsContainer.innerHTML = "";
    if (articles.length === 0) {
      newsContainer.innerHTML = "<p>No articles found for this category.</p>";
      return;
    }

    articles.forEach(article => {
      const card = document.createElement("div");
      card.className = "news-card";

      const title = document.createElement("h3");
      title.textContent = article.title;

      const category = document.createElement("p");
      category.className = "news-category";
      category.textContent = `Category: ${article.category}`;

      const date = document.createElement("p");
      date.className = "news-date";
      date.textContent = `Date: ${article.date || "N/A"}`;

      const content = document.createElement("p");
      content.className = "news-content";
      content.textContent = article.content.slice(0, 250) + "...";

      card.appendChild(title);
      card.appendChild(category);
      card.appendChild(date);
      card.appendChild(content);
      newsContainer.appendChild(card);
    });
  }

  // Filter by category
  categorySelect.addEventListener("change", function () {
    const selected = categorySelect.value;
    if (selected === "All") {
      renderArticles(allArticles);
    } else {
      const filtered = allArticles.filter(article => article.category === selected);
      renderArticles(filtered);
    }
  });
});

document.getElementById("searchForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent form from refreshing the page

    const query = document.getElementById("movieInput").value;
    if (!query.trim()) {
        alert("Please enter a movie name.");
        return;
    }

    try {
        const response = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ search_query: query }),
        });

        if (!response.ok) throw new Error("Failed to fetch recommendations.");

        const data = await response.json();
        const resultsContainer = document.getElementById("results");

        // Clear previous results and display new ones
        resultsContainer.innerHTML = data
            .map((movie) => `<li>${movie.title}</li>`)
            .join("");
        resultsContainer.classList.remove("hidden");
    } catch (error) {
        console.error(error);
        alert("An error occurred. Please try again.");
    }
});

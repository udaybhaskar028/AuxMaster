
const API_BASE = "https://auxmaster.onrender.com";// change later if deployed
const queryInput = document.getElementById("query");
const resultsDiv = document.getElementById("results");
const searchBtn = document.getElementById("searchBtn");

async function search() {
  const q = queryInput.value.trim();
  if (!q) return;
  resultsDiv.innerHTML = `<p class="text-gray-400">Searching for "${q}"...</p>`;

  try {
    const res = await fetch(`${API_BASE}/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q, k: 5 }),
    });

    if (!res.ok) {
      const msg = await res.text();
      resultsDiv.innerHTML = `<p class="text-red-500">Error: ${msg}</p>`;
      return;
    }

    const data = await res.json();
    renderResults(data.results);
  } catch (err) {
    console.error(err);
    resultsDiv.innerHTML = `<p class="text-red-500">Network error</p>`;
  }
}

function renderResults(results) {
  if (!results || results.length === 0) {
    resultsDiv.innerHTML = `<p class="text-gray-400">No recommendations found.</p>`;
    return;
  }

  resultsDiv.innerHTML = results
    .map(
      (r) => `
      <div class="p-4 bg-gray-800 rounded-lg shadow flex justify-between items-center">
        <div>
          <p class="font-semibold">${r.title}</p>
          <p class="text-sm text-gray-400">${r.artist} · ${r.genre}</p>
          <p class="text-xs text-gray-500">Score: ${r.adjusted_score.toFixed(3)}</p>
        </div>
        <div class="space-x-2">
          <button onclick="sendFeedback(${r.id}, true)" class="bg-green-500 hover:bg-green-600 px-3 py-1 rounded text-sm">👍</button>
          <button onclick="sendFeedback(${r.id}, false)" class="bg-red-500 hover:bg-red-600 px-3 py-1 rounded text-sm">👎</button>
        </div>
      </div>
    `
    )
    .join("");
}

async function sendFeedback(trackId, liked) {
  try {
    await fetch(`${API_BASE}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ track_id: trackId, liked }),
    });
  } catch (err) {
    console.error("feedback failed", err);
  }
}

searchBtn.addEventListener("click", search);
queryInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") search();
});

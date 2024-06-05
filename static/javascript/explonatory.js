async function performSearch() {
    const searchType = document.getElementById('searchType').value;
    const searchTerm = document.getElementById('searchTerm').value;
    const checkboxes = document.querySelectorAll('.file-checkbox:checked');
    const selectedFiles = Array.from(checkboxes).map(checkbox => ({
        fileName: checkbox.value,
        fileType: checkbox.getAttribute('data-type')
    }));

    const response = await fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchType, searchTerm, selectedFiles }),
    });

    const results = await response.json();
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = results.map(result => `<p>${result}</p>`).join('');
}

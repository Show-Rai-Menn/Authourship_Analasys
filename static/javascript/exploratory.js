function performSearch() {
    const searchType = document.getElementById('searchType').value;
    const searchTerm = document.getElementById('searchTerm').value;
    const form = document.getElementById('form');
    const data = {
        Q: [],
        K: [],
        searchTerm,
        searchType
    };

    const checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');
    

    checkboxes.forEach((checkbox) => {
        if (checkbox.name === 'Q') {
            data.Q.push(checkbox.value);
        } else if (checkbox.name === 'K') {
            data.K.push(checkbox.value);
        }
    });
    
    fetch('/exploratory/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        const resultTag = document.getElementById('results');
        resultTag.innerHTML = result.html;
    })
    .catch(error => {
        const resultTag = document.getElementById('results');
        resultTag.innerHTML = 'An error occurred: ' + error.message;
    });
}
let count = 0;

function comparison(event) {
    event.preventDefault();
    const form = document.getElementById('form');
    const data = {
        Q: [],
        K: [],
        count: 0
    };
    count++;
    
    const checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');

    checkboxes.forEach((checkbox) => {
        if (checkbox.name === 'Q') {
            data.Q.push(checkbox.value);
        } else if (checkbox.name === 'K') {
            data.K.push(checkbox.value);
        }
    });
    data.count = count;
    
    fetch('/comparison/result', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        const resultTag = document.getElementById('result');
        resultTag.innerHTML = result.html;
    })
    .catch(error => {
        const resultTag = document.getElementById('result');
        resultTag.innerHTML = 'An error occurred: ' + error.message;
    });
}

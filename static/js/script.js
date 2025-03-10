document.getElementById('preferences-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const preferences = document.getElementById('preferences').value.split(',').map(p => p.trim());
    
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ preferences: preferences })
    })
    .then(response => response.json())
    .then(data => {
        const output = `
            <h2>${data.title}</h2>
            <p><strong>Ingredients:</strong> ${data.ingredients.join(', ')}</p>
            <p><strong>Instructions:</strong> ${data.instructions}</p>
        `;
        document.getElementById('recipe-output').innerHTML = output;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('recipe-output').innerHTML = '<p>Error generating recipe. Please try again.</p>';
    });
});
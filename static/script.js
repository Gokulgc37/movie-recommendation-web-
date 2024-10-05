// script.js
document.getElementById('movie-form').addEventListener('submit', function (e) {
    e.preventDefault();
    
    let movieName = document.getElementById('movie-name').value;
    
    fetch(`/recommend?movie_name=${movieName}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        let recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = '<h3>Recommended Movies:</h3>';
        let ul = document.createElement('ul');
        data.forEach(movie => {
            let li = document.createElement('li');
            li.textContent = movie;
            ul.appendChild(li);
        });
        recommendationsDiv.appendChild(ul);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

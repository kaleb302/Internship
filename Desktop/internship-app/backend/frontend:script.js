document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading spinner
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').innerHTML = '';

    const formData = new FormData();
    formData.append('resume', document.getElementById('resume').files[0]);
    formData.append('location', document.getElementById('location').value);
    formData.append('start_date', document.getElementById('startDate').value);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Server error');
        
        const data = await response.json();
        displayResults(data.jobs);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to fetch internships. Check console for details.');
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
});

function displayResults(jobs) {
    const resultsDiv = document.getElementById('results');
    
    if (jobs.length === 0) {
        resultsDiv.innerHTML = '<p>No internships found. Try different filters!</p>';
        return;
    }

    resultsDiv.innerHTML = jobs.map(job => `
        <div class="job-card">
            <h3>${job.title}</h3>
            <p>${job.company} • ${job.location}</p>
            <p>Deadline: ${job.deadline || 'Not specified'}</p>
            <a href="${job.link}" target="_blank" class="apply-button">Apply Now</a>
        </div>
    `).join('');
}
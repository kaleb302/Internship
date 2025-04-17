// Initialize Firebase (v8 compatibility version)
const firebaseConfig = {
    apiKey: "AIzaSyDLDNpM3EQ8m1Tj2utGEx48oFDHrOZj50c",
    authDomain: "ai-intership-finder.firebaseapp.com",
    projectId: "ai-intership-finder",
    storageBucket: "ai-intership-finder.firebasestorage.app",
    messagingSenderId: "368682202393",
    appId: "1:368682202393:web:4d1c5ef1113b4edd258188",
    measurementId: "G-TZ4XK4YMYN"
  };
  
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  const auth = firebase.auth();
  const analytics = firebase.analytics();
  
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
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      });
  
      // Handle HTTP errors
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error: ${response.status} - ${errorText}`);
      }
  
      const data = await response.json();
      displayResults(data.jobs);
  
    } catch (error) {
      console.error('Full error details:', {
        error: error.message,
        stack: error.stack,
      });
      alert(`Error: ${error.message}`);
      analytics.logEvent('upload_error', { error: error.message });
    } finally {
      // Hide loading spinner
      document.getElementById('loading').classList.add('hidden');
    }
  });
  
  function displayResults(jobs) {
    const resultsDiv = document.getElementById('results');
    
    if (!jobs || jobs.length === 0) {
      resultsDiv.innerHTML = '<p class="error">No internships found. Try different filters!</p>';
      return;
    }
  
    resultsDiv.innerHTML = jobs.map(job => `
      <div class="job-card">
        <h3>${job.title || 'Position Not Specified'}</h3>
        <div class="job-details">
          <p class="company">${job.company || 'Company Not Specified'}</p>
          <p class="location">📍 ${job.location || 'Location Not Specified'}</p>
          ${job.link ? `<a href="${job.link}" target="_blank" class="apply-btn">Apply Now →</a>` : ''}
        </div>
      </div>
    `).join('');
  }
  
  // Initial setup - clear previous state
  document.getElementById('loading').classList.add('hidden');
  
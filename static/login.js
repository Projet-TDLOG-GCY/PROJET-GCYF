// login.js

// Function to handle user signup
function handleSignup() {
    // ... (code for handling signup form submission)
  }
  
  // Function to handle user login
  function handleLogin() {
    // ... (code for handling login form submission)
  }
  
  // Event listener for signup form
  const signupForm = document.getElementById('signup-form');
  signupForm.addEventListener('submit', (event) => {
    event.preventDefault();
    handleSignup();
  });
  
  // Event listener for login form
  const loginForm = document.getElementById('login-form');
  loginForm.addEventListener('submit', (event) => {
    event.preventDefault();
    handleLogin();
  });
  
const promptForm = document.getElementById("prompt-form");
const submitButton = document.getElementById("submit-button");
const questionButton = document.getElementById("question-button");
const messagesContainer = document.getElementById("messages-container");
const mainContainer = document.getElementById("main-container");
const prompto = document.getElementById("prompt");
const resetButton = document.getElementById("reset-button");
const aboutusContent = document.getElementById("about-us-content");


const appendHumanMessage = (message) => {
  const humanMessageElement = document.createElement("div");
  humanMessageElement.classList.add("message", "message-human");
  humanMessageElement.innerHTML = message;
  messagesContainer.appendChild(humanMessageElement);
};



// Fonction pour activer/désactiver le mode sombre
function toggleDarkMode() {
  const body = document.body;
  mainContainer.classList.toggle('dark-mode');
  body.classList.toggle('dark-mode');
  prompto.classList.toggle('dark-mode');
  promptForm.classList.toggle('dark-mode');
  submitButton.classList.toggle('dark-mode');
  questionButton.classList.toggle('dark-mode');
  messagesContainer.classList.toggle('dark-mode');
  resetButton.classList.toggle('dark-mode');
  aboutusContent.classList.toggle('dark-mode');



  // Stocker l'état du mode sombre dans localStorage
  if (mainContainer.classList.contains('dark-mode')) {
    localStorage.setItem('darkMode', 'enabled');
  } else {
    localStorage.setItem('darkMode', 'disabled');
  }
  if (body.classList.contains('dark-mode')) {
    localStorage.setItem('darkMode', 'enabled');
  } else {
    localStorage.setItem('darkMode', 'disabled');
  }

  if (prompto.classList.contains('dark-mode')) {
    localStorage.setItem('darkMode', 'enabled');
  } else {
    localStorage.setItem('darkMode', 'disabled');
  }

  if (promptForm.classList.contains('dark-mode')) {
    localStorage.setItem('darkMode', 'enabled');
  } else {
    localStorage.setItem('darkMode', 'disabled');
  }

  if (submitButton.classList.contains('dark-mode')) {
    localStorage.setItem('darkMode', 'enabled');
  } else {
    localStorage.setItem('darkMode', 'disabled');
  }
  if (questionButton.classList.contains('dark-mode')) {
    localStorage.setItem('darkMode', 'enabled');
  } else {
    localStorage.setItem('darkMode', 'disabled');
  }
  if (messagesContainer.classList.contains('dark-mode')) {
    localStorage.setItem('darkMode', 'enabled');
  } else {
    localStorage.setItem('darkMode', 'disabled');
  }
  if (aboutusContent.classList.contains('dark-mode')) {
    localStorage.setItem('darkMode', 'enabled');
  } else {
    localStorage.setItem('darkMode', 'disabled');
  }
}

// Vérifier l'état du mode sombre lors du chargement de la page
document.addEventListener('DOMContentLoaded', () => {
  const darkModeState = localStorage.getItem('darkMode');
  if (darkModeState === 'enabled') {
    toggleDarkMode();
  }
});

// Associer la fonction de bascule à un bouton ou à un événement de votre choix
const darkModeButton = document.getElementById('dark-mode-toggle');
darkModeButton.addEventListener('click', toggleDarkMode);





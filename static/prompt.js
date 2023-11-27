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




const appendAIMessage = async (messagePromise) => {
  // Add a loader to the interface
  const loaderElement = document.createElement("div");
  loaderElement.classList.add("message");
  loaderElement.innerHTML =
    "<div class='loader'><div></div><div></div><div></div>";
  messagesContainer.appendChild(loaderElement);

  // Await the answer from the server
  const messageToAppend = await messagePromise();

  // Replace the loader with the answer
  loaderElement.classList.remove("loader");
  loaderElement.innerHTML = messageToAppend;
};

const handlePrompt = async (event) => {
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  promptForm.reset();

  let url = "/prompt";
  if (questionButton.dataset.question !== undefined) {
    url = "/answer";
    data.append("question", questionButton.dataset.question);
    delete questionButton.dataset.question;
    questionButton.classList.remove("hidden");
    submitButton.innerHTML = "Message";
  }

  appendHumanMessage(data.get("prompt"));

  await appendAIMessage(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    return result.answer;
  });
};

promptForm.addEventListener("submit", handlePrompt);

const handleQuestionClick = async (event) => {
  appendAIMessage(async () => {
    const response = await fetch("/question", {
      method: "GET",
    });
    const result = await response.json();
    const question = result.answer;

    questionButton.dataset.question = question;
    questionButton.classList.add("hidden");
    submitButton.innerHTML = "Répondre à la question";
    return question;
  });
};

questionButton.addEventListener("click", handleQuestionClick);


const handleResetButton = (event) => {
  while (messagesContainer.children.length > 1) {
    messagesContainer.removeChild(messagesContainer.lastChild);
  }
}

resetButton.addEventListener("click", handleResetButton);

// function calculateCDF(value) {
//           // Exemple avec une distribution normale standard
//           return math.erf(value / Math.sqrt(2)) / 2 + 0.5;
//         }

document.addEventListener("DOMContentLoaded", function () {
  const calculatePriceButton = document.getElementById("calculate-price");
  const resultDiv = document.getElementById("result");

  calculatePriceButton.addEventListener("click", function () {
    // Récupération des valeurs des paramètres
    const param1Value = parseFloat(document.getElementById("param1").value);
    const param2Value = parseFloat(document.getElementById("param2").value);    

    // Vérification si les valeurs sont des nombres valides
    if (!isNaN(param1Value) && !isNaN(param2Value)) {
      // Calcul du prix (à modifier selon votre fonction de calcul)
      const price =param1Value*param2Value*param1Value +2; // Exemple de calcul
      //const cdfResult = calculateCDF(param1Value + param2Value);

      // Affichage du prix calculé
      resultDiv.textContent = `Le prix est : ${price}`;
    } else {
      // Affichage d'un message si les valeurs ne sont pas des nombres valides
      resultDiv.textContent = "Veuillez saisir des nombres valides pour les paramètres.";
    }
  });
});

// document.addEventListener("DOMContentLoaded", function () {
//   const calculateCDFButton = document.getElementById("calculate-price");
//   const cdfResultDiv = document.getElementById("result");

//   calculateCDFButton.addEventListener("click", function () {
//     // Récupération des valeurs des paramètres
//     const param1Value = parseFloat(document.getElementById("param1").value);
//     const param2Value = parseFloat(document.getElementById("param2").value);

//     // Vérification si les valeurs sont des nombres valides
//     if (!isNaN(param1Value) && !isNaN(param2Value)) {
//       // Calcul de la fonction de répartition (CDF) pour param1 + param2 (à ajuster selon la distribution souhaitée)
//       const cdfResult = calculateCDF(param1Value + param2Value);

//       // Affichage du résultat de la CDF
//       cdfResultDiv.textContent = `La fonction de répartition (CDF) est : ${cdfResult}`;
//     } else {
//       // Affichage d'un message si les valeurs ne sont pas des nombres valides
//       cdfResultDiv.textContent = "Veuillez saisir des nombres valides pour les paramètres.";
//     }
//   });

//   // Fonction pour calculer la CDF (à ajuster selon la distribution souhaitée)
//   function calculateCDF(value) {
//     // Exemple avec une distribution normale standard
//     return math.erf(value / Math.sqrt(2)) / 2 + 0.5;
//   }
// });

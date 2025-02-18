const currentURL = window.location.href;
// const currentURL = `http://23.20.175.90/api/api/menu-filter/by-horekaclient-id/1`;
const segments = currentURL.split("/");
const indexURL = segments[segments.length - 1]; // Get the last part of the URL

const bodyBg = document.getElementById("body-bg");
const rTitle = document.getElementById("r-title");
const rLogo = document.getElementById("r-logo");
const wMessage = document.getElementById("welcome-message");
const languages = document.querySelectorAll(".lang");

// -------------------------------------------------------------

let cafeIndex = localStorage.setItem("cafeIdIndex", indexURL);
let cafeLang = localStorage.setItem("language", "en");

languages.forEach((lang) => {
  lang.addEventListener("click", () => {
    for (let i = 0; i < languages.length; i++) {
      languages[i].classList.remove("active");
    }

    lang.classList.add("active");
    cafeLang = lang.getAttribute("data-lang");
    localStorage.setItem("language", cafeLang);
  });
});

async function FetchingAPI(link) {
  try {
    const response = await fetch(link);
    const data = await response.json();

    bodyBg.src = data.image_src;
    rTitle.innerText = data.name;
    rLogo.src = data.logo;
    wMessage.innerText = `Welcome to ${data.name}`;
  } catch (error) {
    console.log("Error fetching URL", error);
  }
}

FetchingAPI(
  `http://23.20.175.90/api/api/menu-filter/by-horekaclient-id/${indexURL}`
);

// FetchingAPI(`http://23.20.175.90/api/api/menu-filter/by-horekaclient-id/1`);

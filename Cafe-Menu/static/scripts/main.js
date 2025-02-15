// const currentURL = window.location.href;
const currentURL = `http://23.20.175.90/api/api/menu-filter/by-horekaclient-id/1`;

console.log(currentURL);
const bodyBg = document.getElementById("body-bg");
const rTitle = document.getElementById("r-title");
const rLogo = document.getElementById("r-logo");
const wMessage = document.getElementById("welcome-message");
const languages = document.querySelectorAll(".lang");

let currentLang = "English";

const pageInfoData = {
  cafeIdIndexArray: currentURL.lastIndexOf("/"),
  lang: currentLang,
};

languages.forEach((lang, index) => {
  lang.addEventListener("click", () => {
    for (let i = 0; i < languages.length; i++) {
      languages[i].classList.remove("active");
    }

    lang.classList.add("active");

    pageInfoData.lang = lang.innerText;
    currentLang = lang.innerText;

    localStorage.setItem("horecaData", JSON.stringify(pageInfoData));
    console.log(localStorage.getItem("horecaData"));
  });
});

async function FetchingAPI(link) {
  try {
    const response = await fetch(link);
    const data = await response.json();

    console.log(data);
    bodyBg.src = data.image_src;
    rTitle.innerText = data.name;
    rLogo.src = data.logo;
    wMessage.innerText = `Welcome to ${data.name}`;
  } catch (error) {
    console.log("Error fetching URL", error);
  }
}

// FetchingAPI(
//   `http://23.20.175.90/api/api/menu-filter/by-horekaclient-id/${cafeIdIndex}`
// );

FetchingAPI(`http://23.20.175.90/api/api/menu-filter/by-horekaclient-id/1`);

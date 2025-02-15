const searchBtn = document.getElementById("searchBtn");
const searchBar = document.getElementById("searchBar");
const menuTitle = document.getElementById("menuTitle");

searchBtn.addEventListener("click", () => {
  if (searchBar.className === "disabled-searchbar") {
    searchBar.className = "enabled-searchbar";
    menuTitle.className = "title-off";
  } else {
    menuTitle.className = "title-on";
    searchBar.className = "disabled-searchbar";
  }
});

// ------------------------------------------------------------

const menuLinks = document.querySelectorAll(".link");

menuLinks.forEach((link) => {
  link.addEventListener("click", () => {
    for (let i = 0; i < menuLinks.length; i++) {
      menuLinks[i].classList.remove("active");
    }

    link.classList.add("active");
  });
});

// ----------------------------------------------------------------------

const Food_API_Link =
  "http://23.20.175.90/api/api/menu-filter/by-kind/food?horekaclient_id=";
const foodCont = document.getElementById("foodCont");

async function foodCategories(link, category) {
  try {
    const response = await fetch(link + localStorage.getItem("horecaID"));
    const data = await response.json();

    for (let i = 0; i < data.length; i++) {
      foodCont.innerHTML += `<div class="item">
                              <div class="likeBtn">
                                <img src="../static/icons/liked.svg" alt="liked" />
                              </div>
                              <img
                                src="${data[i].image_src}"
                                alt="meal"
                                class="item-img"
                              />
                              <div class="info">
                                <p class="name">${data[i].name}</p>
                                <p class="price">AMD${data[i].price}</p>
                              </div>
                            </div>`;
    }
  } catch (error) {
    console.log("Error fetchind api", error);
  }
}

foodCategories(Food_API_Link);

foodCont.addEventListener("click", (event) => {
  const item = event.target.closest(".item");
  if (!item) return;

  const name = item.querySelector(".name").textContent;
  const price = item.querySelector(".price").textContent;
  const imgURL = item.querySelector(".item-img").src;

  const mealInfo = {
    name,
    price,
    imgURL,
  };

  localStorage.setItem("selectedMeal", JSON.stringify(mealInfo));
  window.location.href = "./about-meal.html";
});

// ------------------------------------------------------------

const Salad_API_Link =
  "http://23.20.175.90/api/api/menu-filter/by-kind/salad?horekaclient_id=";
const saladCont = document.getElementById("saladCont");

async function saladCategories(link) {
  try {
    const response = await fetch(link + localStorage.getItem("horecaID"));
    const data = await response.json();

    for (let i = 0; i < data.length; i++) {
      saladCont.innerHTML += `<div class="item">
                              <div class="likeBtn">
                                <img src="../static/icons/liked.svg" alt="liked" />
                              </div>
                              <img
                                src="${data[i].image_src}"
                                alt="meal"
                                class="item-img"
                              />
                              <div class="info">
                                <p class="name">${data[i].name}</p>
                                <p class="price">AMD${data[i].price}</p>
                              </div>
                            </div>`;
    }
  } catch (error) {
    console.log("Error fetchind api", error);
  }
}

saladCategories(Salad_API_Link);

saladCont.addEventListener("click", (event) => {
  const item = event.target.closest(".item");
  if (!item) return;

  const name = item.querySelector(".name").textContent;
  const price = item.querySelector(".price").textContent;
  const imgURL = item.querySelector(".item-img").src;

  const mealInfo = {
    name,
    price,
    imgURL,
  };

  localStorage.setItem("selectedMeal", JSON.stringify(mealInfo));
  window.location.href = "./about-meal.html";
});

// ------------------------------------------------------------

const Drink_API_Link =
  "http://23.20.175.90/api/api/menu-filter/by-kind/drink?horekaclient_id=";
const drinkCont = document.getElementById("drinkCont");

async function drinkCategories(link) {
  try {
    const response = await fetch(link + localStorage.getItem("horecaID"));
    const data = await response.json();

    for (let i = 0; i < data.length; i++) {
      drinkCont.innerHTML += `<div class="item">
                              <div class="likeBtn">
                                <img src="../static/icons/liked.svg" alt="liked" />
                              </div>
                              <img
                                src="${data[i].image_src}"
                                alt="meal"
                                class="item-img"
                              />
                              <div class="info">
                                <p class="name">${data[i].name}</p>
                                <p class="price">AMD${data[i].price}</p>
                              </div>
                            </div>`;
    }
  } catch (error) {
    console.log("Error fetchind api", error);
  }
}

drinkCategories(Drink_API_Link);

drinkCont.addEventListener("click", (event) => {
  const item = event.target.closest(".item");
  if (!item) return;

  const name = item.querySelector(".name").textContent;
  const price = item.querySelector(".price").textContent;
  const imgURL = item.querySelector(".item-img").src;

  const mealInfo = {
    name,
    price,
    imgURL,
  };

  localStorage.setItem("selectedMeal", JSON.stringify(mealInfo));
  window.location.href = "./about-meal.html";
});

// ------------------------------------------------------------

const Dessert_API_Link =
  "http://23.20.175.90/api/api/menu-filter/by-kind/desert?horekaclient_id=";
const dessertCont = document.getElementById("dessertCont");

async function dessertCategories(link) {
  try {
    const response = await fetch(link + localStorage.getItem("horecaID"));
    const data = await response.json();

    for (let i = 0; i < data.length; i++) {
      dessertCont.innerHTML += `<div class="item">
                              <div class="likeBtn">
                                <img src="../static/icons/liked.svg" alt="liked" />
                              </div>
                              <img
                                src="${data[i].image_src}"
                                alt="meal"
                                class="item-img"
                              />
                              <div class="info">
                                <p class="name">${data[i].name}</p>
                                <p class="price">AMD${data[i].price}</p>
                              </div>
                            </div>`;
    }
  } catch (error) {
    console.log("Error fetchind api", error);
  }
}

dessertCategories(Dessert_API_Link);

dessertCont.addEventListener("click", (event) => {
  const item = event.target.closest(".item");
  if (!item) return;

  const name = item.querySelector(".name").textContent;
  const price = item.querySelector(".price").textContent;
  const imgURL = item.querySelector(".item-img").src;

  const mealInfo = {
    name,
    price,
    imgURL,
  };

  localStorage.setItem("selectedMeal", JSON.stringify(mealInfo));
  window.location.href = "./about-meal.html";
});

// -------------------------------------------------------------------------

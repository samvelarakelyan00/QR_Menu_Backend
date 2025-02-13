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

// ------------------------------------------------------------

const menuItems = document.querySelectorAll(".item");
const menuItemsNames = document.querySelectorAll(".name");
const menuItemsPrices = document.querySelectorAll(".price");
const menuItemsImages = document.querySelectorAll(".item-img");

menuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    const mealInfo = {
      name: menuItemsNames[index].textContent,
      price: menuItemsPrices[index].textContent,
      imgURL: menuItemsImages[index].src,
    };

    localStorage.setItem("selectedMeal", JSON.stringify(mealInfo));

    window.location.href = "./about-meal.html";
  });
});

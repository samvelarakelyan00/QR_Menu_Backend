const parsedLocalData = JSON.parse(localStorage.getItem("selectedMeal"));

// ---------------------------------------------------------------

const pageURLIndex = localStorage.getItem("cafeIdIndex");

// ---------------------------------------------------------------

const backPreviousPageBtn = document.querySelector(".backPreviousPage");
const backHomePageBtn = document.querySelector(".backHomePage");
const orderLink = document.getElementById("orderLink");

backPreviousPageBtn.setAttribute(
  "href",
  `http://23.20.175.90/api/cafe/menu/get-menu`
);
backHomePageBtn.setAttribute("href", `http://23.20.175.90/api/${pageURLIndex}`);
orderLink.setAttribute("href", "#");

// ---------------------------------------------------------

const mealName = document.getElementById("name");
const mealPrice = document.getElementById("price");
const mealIMG = document.getElementById("foodImg");
const mealDesc = document.getElementById("mealDescription");

// ---------------------------------------------------------------

const About_Meal_API_Link =
  "http://23.20.175.90/api/api/menu-filter/by-product-id/";
const Meal_API_Link_Middle_Part = parsedLocalData.itemID;
const Meal_API_Link_Last_Part = "?horekaclient_id=";
const cafeURLIndex = localStorage.getItem("cafeIdIndex");

async function fetchingMealInfo(link) {
  try {
    const resp = await fetch(link);
    const data = await resp.json();

    mealName.innerText = data.name;
    mealPrice.innerText = data.price + " " + "AMD";
    foodImg.src = data.image_src;
    mealDesc.innerText = data.description;
  } catch (error) {
    console.log("Error fetching data", error);
  }
}

fetchingMealInfo(
  About_Meal_API_Link +
    Meal_API_Link_Middle_Part +
    Meal_API_Link_Last_Part +
    cafeURLIndex
);

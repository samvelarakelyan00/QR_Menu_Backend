const parsedLocalData = JSON.parse(localStorage.getItem("selectedMeal"));

// ---------------------------------------------------------------

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

console.log(Meal_API_Link_Middle_Part);

async function fetchingMealInfo(link) {
  try {
    const resp = await fetch(link);
    const data = await resp.json();

    console.log(data);

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

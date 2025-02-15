const selectedMeal = localStorage.getItem("selectedMeal");
const selectedMealInfo = JSON.parse(selectedMeal);
const selectedMealImgUrl = selectedMealInfo.imgURL.slice(22);
const selectedMealName = document.getElementById("name");
const selectedMealPrice = document.getElementById("price");
const selectedMealImg = document.getElementById("foodImg");

selectedMealName.innerText = selectedMealInfo.name;
selectedMealPrice.innerText = selectedMealInfo.price;
selectedMealImg.src = "../" + selectedMealImgUrl;

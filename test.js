const url = "http://23.20.175.90/api/users";
let response = fetch(url);

if (response.ok) { // если HTTP-статус в диапазоне 200-299
  // получаем тело ответа (см. про этот метод ниже)
  let json = response.json();
  console.log(json)
} else {
  alert("Ошибка HTTP: " + response.status);
}


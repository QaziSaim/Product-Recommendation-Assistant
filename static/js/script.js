const API =
"http://localhost:8000";

async function recommend(){

const budget =
document.getElementById("budget").value;

const category =
document.getElementById("category").value;

const response =
await fetch(`${API}/recommend`,{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
budget,
category
})

});

const data =
await response.json();

const container =
document.getElementById("products");

container.innerHTML="";

data.products.forEach(product=>{

container.innerHTML += `
<div class="card">
<img src="${product.image}">
<h3>${product.name}</h3>
<p>${product.description}</p>
<div class="price">
₹${product.price}
</div>
</div>
`;

});

}

async function chat(){

const query =
document.getElementById("query").value;

const response =
await fetch(`${API}/chat`,{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
query
})

});

const data =
await response.json();

const messages =
document.getElementById("messages");

messages.innerHTML += `
<div class="message user">
${query}
</div>
`;

messages.innerHTML += `
<div class="message bot">
${data.response}
</div>
`;

}
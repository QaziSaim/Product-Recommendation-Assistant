const API = "http://localhost:8000";

/* -----------------------------
   Budget Slider
----------------------------- */

const budgetSlider =
document.getElementById("budget");

const budgetValue =
document.getElementById("budgetValue");

budgetSlider.addEventListener("input", () => {

    budgetValue.innerText =
    `₹${Number(budgetSlider.value).toLocaleString()}`;

});

/* -----------------------------
   Product Recommendation
----------------------------- */

async function recommend() {

    const budget =
    document.getElementById("budget").value;

    const category =
    document.getElementById("category").value;

    const container =
    document.getElementById("products");

    const messages =
    document.getElementById("messages");

    messages.innerHTML = `
        <div class="loading">
            Finding best products...
        </div>
    `;

    try {

        const response =
        await fetch(`${API}/recommend`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                budget: parseInt(budget),
                category: category
            })

        });

        const data =
        await response.json();

        messages.innerHTML = `
            <h3>AI Recommendation</h3>
            <p>
                ${data.response}
            </p>
        `;

        container.innerHTML = "";

        if (!data.products ||
            data.products.length === 0) {

            container.innerHTML = `
                <h3>
                    No products found
                </h3>
            `;

            return;
        }

        data.products.forEach(product => {

            container.innerHTML += `

            <div class="product-card">

                <img
                    src="${product.image}"
                    alt="${product.name}"
                >

                <div class="card-body">

                    <h3>
                        ${product.name}
                    </h3>

                    <p>
                        ${product.description}
                    </p>

                    <div class="price">
                        ₹${Number(product.price).toLocaleString()}
                    </div>

                    <div class="rating">
                        ⭐ ${product.rating}
                    </div>

                    <button
                        class="view-btn"
                        onclick="viewProduct('${product.name}')"
                    >
                        View Product
                    </button>

                </div>

            </div>

            `;
        });

    } catch (error) {

        console.error(error);

        messages.innerHTML = `
            <p>
                Error fetching recommendations.
            </p>
        `;
    }
}

/* -----------------------------
   AI Chat
----------------------------- */

async function chat() {

    const queryInput =
    document.getElementById("query");

    const query =
    queryInput.value.trim();

    if (!query) return;

    const messages =
    document.getElementById("messages");

    messages.innerHTML = `
        <div class="user-message">
            ${query}
        </div>

        <div class="bot-message">
            Thinking...
        </div>
    `;

    try {

        const response =
        await fetch(`${API}/chat`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                query
            })

        });

        const data =
        await response.json();

        messages.innerHTML = `

            <div class="user-message">
                ${query}
            </div>

            <div class="bot-message">
                ${data.response}
            </div>

        `;

        if (data.products) {

            renderProducts(
                data.products
            );
        }

        queryInput.value = "";

    } catch (error) {

        console.error(error);

        messages.innerHTML = `
            <div class="bot-message">
                Something went wrong.
            </div>
        `;
    }
}

/* -----------------------------
   Render Product Cards
----------------------------- */

function renderProducts(products) {

    const container =
    document.getElementById("products");

    container.innerHTML = "";

    products.forEach(product => {

        container.innerHTML += `

        <div class="product-card">

            <img
                src="${product.image}"
                alt="${product.name}"
            >

            <div class="card-body">

                <h3>
                    ${product.name}
                </h3>

                <p>
                    ${product.description}
                </p>

                <div class="price">
                    ₹${Number(product.price).toLocaleString()}
                </div>

                <div class="rating">
                    ⭐ ${product.rating}
                </div>

                <button
                    class="view-btn"
                    onclick="viewProduct('${product.name}')"
                >
                    View Product
                </button>

            </div>

        </div>

        `;
    });
}

/* -----------------------------
   Product Detail
----------------------------- */

function viewProduct(productName) {

    alert(
        `Selected Product:\n${productName}`
    );

}

/* -----------------------------
   Enter Key Support
----------------------------- */

document
.getElementById("query")
.addEventListener("keypress", e => {

    if (e.key === "Enter") {

        chat();

    }

});
// Eventlistener for Add Nail Button
document.getElementById("skuAdder").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const formData = {
        type: document.getElementById("NailTypeInput").value,
        rating: parseInt(document.getElementById("nailRatingInput").value),
        price: parseFloat(document.getElementById("nailPriceInput").value),
        sold: 0
    };

    fetch("/nail_api", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to submit form.")
        }
        return response.json()
    })
    .catch(error => {
        console.error("Error: Cannot add Nail")
    });
    updatePage();
});

// Eventlistener for nail action buttons
document.getElementById("nailDisplay").addEventListener("click", function(event) {
    const button = event.target

    if (button && button.tagName === "BUTTON") {
        const nailID = button.getAttribute("data-id")
        if (button.id === "sellNailButton"){
            sellNail(nailID)
        }
        else if (button.id === "buybackNailButton"){
            buybackNail(nailID)
        }
        else if (button.id === "deleteNailButton"){
            deleteNail(nailID)
        }
        updatePage();
    }
});

function sellNail(nailID) {
    fetch("/nail_api/" + nailID)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {

            data.sold += 1

            fetch("/nail_api/" + nailID, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to submit form.")
                }
                return response.json()
            })
            .catch(error => {
                console.error("Error:", error)
            });
        })
        .catch(error => {
            console.error("Error: Cannot sell Nail");
        });
}

function buybackNail(nailID){
    fetch("/nail_api/" + nailID)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            if (data.sold > 0){
                data.sold -= 1
                fetch("/nail_api/" + nailID, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error("Failed to submit form.")
                        }
                        return response.json()
                    })
                    .catch(error => console.error("Error:", error));
            }
            else {
                throw new error('Cannot buyback below 0 sold!')
            }
        })
        .catch(error => {
            console.error("Error: Cannot buyback Nail");
        });
}

function deleteNail(nailID) {
    fetch("/nail_api/" + nailID)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            fetch("/nail_api/" + nailID, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to submit form.")
                }
                return response.json()
            })
            .catch(error => {
                console.error("Error:", error)
            });
        })
        .catch(error => {
            console.error("Error: Cannot delete Nail");
        });
}


function updateTable() {
    fetch("/nail_api")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector("#nailTable tbody");
            tableBody.innerHTML = "";

            data.forEach(nail => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${nail.id}</td>
                    <td>${nail.type}</td>
                    <td>${nail.rating}</td>
                    <td>${nail.price}</td>
                    <td>${nail.sold}</td>
                    <td scope="col">
                        <button class="btn btn-primary" id="sellNailButton" data-id=${nail.id}>
                            Sell Nail
                        </button>
                        <button class="btn btn-secondary" id="buybackNailButton" data-id=${nail.id}>
                            Buyback
                        </button>
                        <button class="btn btn-danger" id="deleteNailButton" data-id=${nail.id}>
                            Delete
                        </button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error:", error));
}

function updatePrice() {
    fetch("/sold_api")
        .then(response => response.json())
        .then(data => {
            price = parseFloat(data).toFixed(2)
            const divBody = document.querySelector("#soldPrice h3");
            divBody.innerHTML = "";

            const priceDisplay = document.createElement("h3")
            priceDisplay.innerText = "Total Sales: $" + price
            divBody.appendChild(priceDisplay);
        })
        .catch(error => console.error("Error:", error));
}

function updatePage() {
    setTimeout(() => {
        updateTable();
        updatePrice();
    }, 10);
}

updatePage();

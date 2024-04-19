// Eventlistener for Add Nail Button
document.getElementById("skuAdder").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const formData = {
        type: document.getElementById("NailTypeInput").value,
        stock: parseInt(document.getElementById("nailStockInput").value),
        price: parseFloat(document.getElementById("nailPriceInput").value),
        sold: 0
    };

    if (isNaN(formData.stock) || formData.stock < 1){
        formData.stock = 10
    }

    fetch("/nail_api", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.status === 400) {
            alert("Error: Nail already exists!");
        }
        else if (!response.ok) {
            throw new Error("Failed to submit form.");
        }
        return response.json()
    })
    .catch(error => {
        console.error("Error: Cannot add Nail");
    });
    document.getElementById("skuAdder").reset();
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


// Eventlistener for reset ledger button
document.getElementById("resetLedger").addEventListener("click", function(event) {
    fetch(`/ledger_api`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to reset ledger!");
        }
        return response.json()
    })
    .catch(error => {
        console.error("Error:", error);
    });
    updatePage();
});

function sellNail(nailID) {
    fetch(`/nail_api/${nailID}/sell`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (response.status === 400){
            alert("Nail out of stock!")
        }
        else if (!response.ok) {
            throw new Error("Failed to sell Nail.");
        }
        return response.json()
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function buybackNail(nailID){
    fetch(`/nail_api/${nailID}/buyback`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (response.status === 400){
            alert("Canot buy nail if none sold!")
        }
        else if (!response.ok) {
            throw new Error("Failed to buyback Nail.");
        }
        return response.json()
    })
    .catch(error => {
        console.error("Error:", error);
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
                    <td>${nail.stock}</td>
                    <td>$${nail.price}</td>
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


function updateSales() {
    fetch("/ledger_api/transactions")
        .then(response => {
            if (!response.ok) {
                const divBody = document.querySelector("#soldPrice h3");
                divBody.innerHTML = '<h3>Total Sales: $0</h3>';
                throw new Error("Unable to optain ledger entries!");
            }
            return response.json();
        })
        .then(data => {
            let soldTotal = 0;
            let boughtTotal = 0;

            if (data.detail != "No entries in ledger"){
                let soldLedger = [];
                let boughtLedger = [];

                data.forEach((transactionType, transactionIndex) => {
                    transactionType.forEach(transaction => {
                        const [transactionNumber, nailType, price] = transaction;
                        const roundedPrice = Math.round((price + Number.EPSILON) * 100) / 100
                        const total = transactionNumber * roundedPrice;
                        const transactionString = `${transactionNumber}X ${nailType} @ $${roundedPrice}`
                        if (transactionIndex === 0) {
                            soldLedger.push("SELL " + transactionString);
                            soldTotal += total;
                        }
                        else {
                            boughtLedger.push("BUY " + transactionString);
                            boughtTotal += total;
                        }
                    })
                })


                const divBody = document.querySelector("#soldPrice h3");
                divBody.innerHTML = "";

                const priceDisplay = document.createElement("h3");
                priceDisplay.dataset.bsToggle = "tooltip";
                priceDisplay.dataset.bsPlacement = "top";
                priceDisplay.dataset.html = "true";

                let toolTipList = '<h3>Ledger:</h3>'

                soldLedger.forEach(item => {
                    toolTipList += `${item}<br>`;
                })

                boughtLedger.forEach(item => {
                    toolTipList += `${item}<br>`;
                })



                priceDisplay.title = toolTipList;

                priceDisplay.innerText = "Total Sales: $" + Math.round(((soldTotal - boughtTotal) + Number.EPSILON) * 100) / 100;

                var toolTip = new bootstrap.Tooltip(priceDisplay)

                divBody.appendChild(priceDisplay);
            }


        })
        .catch(error => console.error("Error:", error));
}

function updatePage() {
    setTimeout(() => {
        updateTable();
        updateSales();
    }, 10);
}

updatePage();

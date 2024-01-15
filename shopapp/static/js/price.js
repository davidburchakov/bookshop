let minValue = document.getElementById("min-value");
let maxValue = document.getElementById("max-value");
let minPriceInput = document.getElementById("min_price");
let maxPriceInput = document.getElementById("max_price");

const rangeFill = document.querySelector(".range-fill");

function validateRange() {
    let minPrice = parseInt(inputElements[0].value);
    let maxPrice = parseInt(inputElements[1].value);
    console.log("minPrice:")
    console.log(minPrice)
    if (minPrice > maxPrice) {
        let tempValue = maxPrice;
        maxPrice = minPrice;
        minPrice = tempValue;
    }

    minValue.innerHTML = "$" + minPrice;
    maxValue.innerHTML = "$" + maxPrice;

    // Update hidden input values
    minPriceInput.value = minPrice;
    maxPriceInput.value = maxPrice;
}

const inputElements = document.querySelectorAll("input[type='range']");

inputElements.forEach((element) => {
    element.addEventListener("input", validateRange);
});

validateRange();


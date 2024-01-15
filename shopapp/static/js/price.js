let minValue = document.getElementById("min-value");
let maxValue = document.getElementById("max-value");
console.log("min-value: ", minValue)
console.log("max-value: ", maxValue)
let minPriceInput = document.getElementById("min_price");
let maxPriceInput = document.getElementById("max_price");

let defaultMin = 0;
let defaultMax = 200;
minValue.innerHTML = "$" + defaultMin;
maxValue.innerHTML = "$" + defaultMax;

function validateRange() {
    let minPrice = parseInt(inputElements[0].value);
    let maxPrice = parseInt(inputElements[1].value);
    console.log("minPrice:")
    console.log(minPrice)
    console.log("max price: ")
    console.log(maxPrice)
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
console.log("Input Elements:")
console.log(inputElements)

inputElements.forEach((element) => {
    element.addEventListener("input", validateRange);
});

validateRange();
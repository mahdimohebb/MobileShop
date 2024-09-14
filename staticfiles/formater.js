
function FormatPrices(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(element => {
      const price = element.getAttribute('data-price');
      const formattedPrice = parseFloat(price).toLocaleString('en-US');
      element.textContent = formattedPrice + ' تومان ';
    });
  }
  

// function convertToPersianNumber(number) {
//       const persianNumbers = [
//         "۰",
//         "۱",
//         "۲",
//         "۳",
//         "۴",
//         "۵",
//         "۶",
//         "۷",
//         "۸",
//         "۹"
//       ];
    
//       const units = ["", "هزار", "میلیون", "میلیارد"];
    
//       let result = "";
    
//       for (let i = 3; i >= 0; i--) {
//         let currentNumber = Math.floor(number / Math.pow(1000, i));
//         if (currentNumber !== 0) {
//           let currentNumberString = currentNumber.toString().split("").map(digit => persianNumbers[parseInt(digit)]).join("");
//           if (i === 0){result += currentNumberString + " " + units[i] + " ";}else{result += currentNumberString + " " + units[i] + " و ";}
//           number -= currentNumber * Math.pow(1000, i);
//         }
//       }
    
//       result = result.trim().replace(/ و $/, "")
      
//       return result + " تومان ";
//     }
    

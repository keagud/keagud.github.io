
const quotesJson = require('./quotes.json')


document.querySelector("#quote").textContent = (() => {

  const quotesArr = quotesJson.quotes;
  const index = Math.floor(Math.random() * (quotesArr.length));
  
  return quotesArr[index]

})();

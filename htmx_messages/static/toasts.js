;(function () {
  const toastOptions = { delay: 5000 }

  function createToast(message) {
    // Clone the template
    const element = htmx.find("[data-toast-template]").cloneNode(true)
    const success_icon_svg = '<svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/></svg>'
    const warning_icon_svg = '<svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z"/></svg>'
    const danger_icon_svg = '<svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/></svg>'
    const succes_icon_classes = ' text-green-500 bg-green-100 rounded-lg dark:bg-green-800 dark:text-green-200'
    const warning_icon_classes = ' text-yellow-500 bg-yellow-100 rounded-lg dark:bg-yellow-700 dark:text-yellow-200'
    const danger_icon_classes = ' text-red-500 bg-red-100 rounded-lg dark:bg-red-800 dark:text-red-200'
    
    // Remove the data-toast-template attribute
    delete element.dataset.toastTemplate

    // Set the CSS class
    element.id += message.tags
    element.classList.remove('hidden');
    element.classList.add('flex');

    // Set the text
    htmx.find(element, "[data-toast-body]").innerText = message.message
    if (message.tags === 'success') {
      element.classList += ' border-green-500'
      htmx.find(element, "[data-icon-container]").innerHTML = success_icon_svg
      htmx.find(element, "[data-icon-container]").classList += succes_icon_classes
    } else if (message.tags === 'warning') {
      element.classList += ' border-yellow-500'
      htmx.find(element, "[data-icon-container]").innerHTML = warning_icon_svg
      htmx.find(element, "[data-icon-container]").classList += warning_icon_classes
    } else if (message.tags === 'danger') {
      element.classList += ' border-red-500'
      htmx.find(element, "[data-icon-container]").innerHTML = danger_icon_svg
      htmx.find(element, "[data-icon-container]").classList += danger_icon_classes
    }
    // Add the new element to the container
    htmx.find("[data-toast-container]").appendChild(element)

    // Show the toast 
    
  }

  htmx.on("messages", (event) => {
    event.detail.value.forEach(createToast);
    htmx.findAll(".toast:not([data-toast-template])").forEach((element) => {
      setTimeout(function() {
        removeFadeOut(element, 1000)
      }, 5000)
    })
  })
})()

function removeFadeOut( el, speed ) {
  var seconds = speed/1000;
  el.style.transition = "opacity "+seconds+"s ease";

  el.style.opacity = 0;
  setTimeout(function() {
      el.parentNode.removeChild(el);
  }, speed);
}

function removeToast(target) {
  let toastElement = target.closest('.toast');
  removeFadeOut(toastElement, 1000);
}

// Sidebar Selectors
const sideBar     = document.querySelector('#sidebar');
const openButton  = document.querySelector('#open-button');
const closeButton = document.querySelector('#close-button');


// Sidebar Event Listeners
openButton.addEventListener('click', event =>{
    if (!sideBar.classList.contains('active'))
    sideBar.classList.add('active');
});

closeButton.addEventListener('click', event =>{
    if (sideBar.classList.contains('active'))
    sideBar.classList.remove('active');
});

// Accordion Selectors 
const accordionButtons = document.querySelectorAll('.accordion__button');

function closeAccordions () {
    accordionButtons.forEach( button => {
        button.classList.remove('active');
    });
}

// Accordion EventListeners
accordionButtons.forEach( button => {
    button.addEventListener('click', event => {

        if (button.classList.contains('active')){
            button.classList.remove('active');
        } else {
            closeAccordions();
            button.classList.add('active');
        }
    });
});

// Navigation mobile selectors 
const buttonNav  = document.querySelector('.navigation__button');
const navigation = document.querySelector('.navigation-mobile');

buttonNav.addEventListener('click', event => {
    buttonNav.classList.toggle('active');
    navigation.classList.toggle('active');

    // If the navigation is closed then all the accordions will be closed as well
    if( !navigation.classList.contains('active') ) closeAccordions();

});

 

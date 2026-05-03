// Buttons selectors
const modalBtns = document.querySelectorAll('[role="modal-button"]');
const modals    = Array.from(document.querySelectorAll('[role="modal"]'));

function handleCloseModal( event ) {
    // Get the modal of this specific button
    const modal = event.currentTarget.closest('.modal');
    // Hide the modal
    modal.classList.remove('open');
    // Show the scroll bar again
    document.body.style.overflowY = 'scroll';
    // Close all the accordions 
    closeAccordions();
}


function handleModalClick( event ) {

    // Prevent the default behaviour of the links 
    event.preventDefault();
    // Get the modal-button id
    const { id } = event.currentTarget;
    // Close all the modals
    modals.forEach( modal => modal.classList.remove('open') );
    
    // Find the selected modal in the array
    const targetModal = modals.find(
        (modal) => modal.getAttribute('aria-labelledby') === id
    );

    console.log(targetModal);

    // Show the target modal
    targetModal.classList.add('open');
    // Hide the scroll in the body
    document.body.style.overflowY = 'hidden';
    // Get the close button
    const closeBtn = targetModal.querySelector('[role="modal-close"]');
    // Add the event listener to it 
    closeBtn.addEventListener('click', handleCloseModal); 
}

// Attach the event 
modalBtns.forEach( (button) => button.addEventListener( 'click', handleModalClick ) );


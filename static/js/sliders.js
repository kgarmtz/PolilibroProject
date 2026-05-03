// To avoid tree
gsap.registerPlugin(ScrollTrigger);

const animateSlides = () => {
    // Select the sliders 
    const sliders = document.querySelectorAll('.section-unit');
    // Loop over each slide
    sliders.forEach( (slide) => {
        // Select the <div> that holds the image
        const revealImg  = slide.querySelector('[role="slider-image"]');
        const img = revealImg.previousElementSibling;
        // Select the <div> that holds the description
        const revealText = slide.querySelector('[role="slider-content"]');

        const slideTl = gsap.timeline({
            defaults: {duration: 1, ease: "power2.inOut"},
            
            scrollTrigger: {
                trigger: slide,
                markers: true,
                start: 'top center',
                toggleActions: 'play none none reverse',
            },
        });

        slideTl.fromTo( revealImg, { x: "0", scale: 2}, { x: "100%", scale: 1});
        slideTl.fromTo( img, { scale: 2}, { scale: 1}, '-=1');
        slideTl.fromTo( revealText, { x: "0%"}, { x: "110%"}, '-=1');
    });


}

animateSlides();
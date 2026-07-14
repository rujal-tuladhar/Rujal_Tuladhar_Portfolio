

/*==================== MENU SHOW Y HIDDEN ====================*/
const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close')

/*===== MENU SHOW =====*/
/* Validate if constant exists */
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu')
    })
}

/*===== MENU HIDDEN =====*/
/* Validate if constant exists */
if (navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu')
    })
}

/*==================== REMOVE MENU MOBILE ====================*/

const navLink = document.querySelectorAll('.nav__link:not(.dropdown__toggle)')

function linkAction() {
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*==================== ACCORDION SKILLS ====================*/
const skillsContent = document.getElementsByClassName('skills__content'),
    skillsHeader = document.querySelectorAll('.skills__header')

function toggleSkills() {
    let itemClass = this.parentNode.className
    for (i = 0; i < skillsContent.length; i++) {
        skillsContent[i].className = 'skills__content skills__close'
    }

    if (itemClass === 'skills__content skills__close') {
        this.parentNode.className = 'skills__content skills__open'
    }
}

skillsHeader.forEach((el) => {
    el.addEventListener('click', toggleSkills)
})


/*==================== QUALIFICATION TABS ====================*/
const tabs = document.querySelectorAll('[data-target]'),
    tabContents = document.querySelectorAll('[data-content]')

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const target = document.querySelector(tab.dataset.target)

        tabContents.forEach(tabContent => {
            tabContent.classList.remove('qualification__active')
        })

        target.classList.add('qualification__active')

        tab.forEach(tab => {
            tab.classList.remove('qualification__active')
        })
        tab.classList.add('qualification__active')
    })
})


/*==================== SERVICES MODAL ====================*/
const modalViews = document.querySelectorAll('.services__modal'),
    modalBtns = document.querySelectorAll('.services__button'),
    modalCloses = document.querySelectorAll('.services__modal-close')

let modal = function (modalClick) {
    modalViews[modalClick].classList.add('active-modal')
}

modalBtns.forEach((modalBtn, i) => {
    modalBtn.addEventListener('click', () => {
        modal(i)
    })
})

modalCloses.forEach((modalClose) => {
    modalClose.addEventListener('click', () => {
        modalViews.forEach((modalView) => {
            modalView.classList.remove('active-modal')
        })
    })
})

/*==================== PORTFOLIO SWIPER  ====================*/
let swiperPortfolio = new Swiper('.portfolio__container', {
    cssMode: true,
    loop: true,


    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    pagination: {

        clickable: true,

    },


});

/*==================== TESTIMONIAL ====================*/
let swiperTestimonial = new Swiper('.testimonial__container', {
    grabCursor: true,
    spaceBetween: 48,
    loop: true,

    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true,
    },
    breakpoints: {
        568: {
            slidesPerView: 2,
        }
    }

});


/*==================== SCROLL SECTIONS ACTIVE LINK ====================*/
const sections = document.querySelectorAll('section[id]')

function scrollActive() {
    const scrollY = window.pageYOffset

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight
        const sectionTop = current.offsetTop - 50;
        sectionId = current.getAttribute('id')

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.add('active-link')
        } else {
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.remove('active-link')
        }
    })
}
window.addEventListener('scroll', scrollActive)

/*==================== CHANGE BACKGROUND HEADER ====================*/
function scrollHeader() {
    const nav = document.getElementById('header')
    // When the scroll is greater than 200 viewport height, add the scroll-header class to the header tag
    if (this.scrollY >= 80) nav.classList.add('scroll-header'); else nav.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)




/*==================== DARK LIGHT THEME ====================*/
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'uil-sun'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'uil-moon' : 'uil-sun'

// We validate if the user previously chose a topic
if (selectedTheme) {
    // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
    document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
    themeButton.classList[selectedIcon === 'uil-moon' ? 'add' : 'remove'](iconTheme)
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // Add or remove the dark / icon theme
    document.body.classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
})

/*==================== DROPDOWN MENU ====================*/
const dropdownToggle = document.querySelector('.dropdown__toggle')
const dropdownMenu = document.querySelector('.dropdown__menu')
const dropdownItem = document.querySelector('.dropdown') // Select the parent li

if (dropdownToggle) {
    dropdownToggle.addEventListener('click', (e) => {
        // On mobile, let the link work (navigate to services page)
        if (window.innerWidth < 768) {
            return; // Don't toggle dropdown, just follow the link
        }
        // On desktop, toggle dropdown
        dropdownMenu.classList.toggle('show-dropdown')
    })
}


// Close dropdown when mouse leaves the dropdown area (Desktop)
if (dropdownItem) {
    dropdownItem.addEventListener('mouseleave', () => {
        if (window.innerWidth >= 768) {
            dropdownMenu.classList.remove('show-dropdown')
        }
    })
}



/*==================== BLOG SLIDER ====================*/
let swiperBlog = new Swiper('.blog__container', {
    grabCursor: true,
    spaceBetween: 48,
    loop: true,
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
    navigation: {
        nextEl: ".swiper-button-next-blog",
        prevEl: ".swiper-button-prev-blog",
    },
    pagination: {
        el: ".swiper-pagination-blog",
        clickable: true,
        dynamicBullets: true,
    },
    breakpoints: {
        568: {
            slidesPerView: 2,
        }
    }
});

/*==================== LEAD TRACKING ====================*/
/* Fires gtag events so leads (form submits + clicks to the contact form)
   are countable in Google Ads / Google Analytics. A LEAD = a successful
   form submission or a click that takes a visitor to a booking form. */
(function () {
    function initLeadTracking() {
        if (typeof gtag !== 'function') return;

        // Strong lead: a form was actually submitted (FormSubmit forms)
        document.querySelectorAll('form[action*="formsubmit.co"]').forEach(function (form) {
            form.addEventListener('submit', function () {
                var label = form.querySelector('[name="_subject"]');
                gtag('event', 'generate_lead', {
                    event_category: 'lead',
                    event_label: label ? label.value : 'form_submit',
                    value: 1
                });
            });
        });

        // Soft lead / intent: a visitor clicked a CTA that goes to the contact form
        document.querySelectorAll('a[href*="#contact"]').forEach(function (link) {
            link.addEventListener('click', function () {
                gtag('event', 'form_cta_click', {
                    event_category: 'lead',
                    event_label: 'contact_cta',
                    value: 1
                });
            });
        });
    }

    // Run now if the DOM is already parsed (main.js loads at end of body / deferred),
    // otherwise wait for it.
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLeadTracking);
    } else {
        initLeadTracking();
    }
})();

/*==================== AUDIENCE SEGMENTATION ====================*/
/* Tags each visitor with an audience segment so GA4 can build remarketing
   audiences. Priority segment = business owners wanting to grow / automate.
   A page may set window.NT_SEGMENT in its <head> to declare its audience
   (e.g. a seniors post sets 'seniors'); otherwise it's inferred from the URL. */
(function () {
    var seg = window.NT_SEGMENT;
    if (!seg) {
        var p = location.pathname;
        if (p.indexOf('/digital-marketing') === 0 || p.indexOf('google-ads') !== -1) seg = 'growth-marketing';
        else if (p.indexOf('/ai-automation') === 0) seg = 'automation';
        else if (p.indexOf('/website-design') === 0) seg = 'web-design';
        else if (p.indexOf('/amazon-seller') === 0 || p.indexOf('/walmart-seller') === 0) seg = 'ecommerce-seller';
        else seg = 'general';
    }
    window.NT_SEGMENT = seg;
    if (typeof gtag === 'function') {
        gtag('set', 'user_properties', { audience_segment: seg });
        gtag('event', 'segment_view', { audience_segment: seg, page_path: location.pathname });
    }
})();

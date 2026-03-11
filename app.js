const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        } else {
            entry.target.classList.remove('show');
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const studyElements = document.querySelectorAll('.study, .study1, .footer, .call_me, .nout, .btn, .main_text, .project1, .project3');

    studyElements.forEach(el => observer.observe(el));

    window.addEventListener('scroll', () => {
        const scroll = window.scrollY;
        const vh = window.innerHeight;
        const mainSection = document.querySelector('.main');
        const bioSection = document.querySelector('.bio');
        const menu = document.querySelector('.menu');

        if (menu) {
            if (scroll > 100) {
                menu.classList.add('menu-fade');
            } else {
                menu.classList.remove('menu-fade');
            }
        }

        let progress = scroll / vh;

        if (mainSection && bioSection) {
            if (progress <= 1) {
                mainSection.style.opacity = 1 - progress;
                bioSection.style.opacity = progress;
            } else {
                mainSection.style.opacity = 0;
                bioSection.style.opacity = 1;
            }
        }
    });
});


const imgContainer = document.querySelector(".bio_project_img");

setInterval(() => {
    let firstImg = imgContainer.firstElementChild;
    firstImg.remove();
    imgContainer.appendChild(firstImg);
}, 2500);


const form = document.getElementById("contactForm");
const result = document.getElementById("resultMessage");

form.addEventListener("submit", async function(e) {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    result.style.display = "none";
    result.className = "";

    try {
        const response = await fetch("/send", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const res = await response.json();

        result.innerText = res.message;
        result.style.display = "block";

        if (res.success) {
            result.classList.add("success_message");
            form.reset();
        } else {
            result.classList.add("error_message");
        }

    } catch (error) {
        result.innerText = "Помилка з'єднання із сервером.";
        result.style.display = "block";
        result.classList.add("error_message");
    }
});
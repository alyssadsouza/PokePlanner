document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".show_view").forEach((btn) => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".view").forEach((div) => {
                div.classList.add("hidden");
            })
            document.querySelector(`#${btn.dataset.div}`).classList.remove("hidden");
        })
    })

})
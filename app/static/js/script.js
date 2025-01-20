document.addEventListener("DOMContentLoaded", () => {
    // the box containing the link for the tabs
    const boxs = document.querySelectorAll(".box");
    const currentPath = window.location.pathname;

    // check the path of the link included in each box
    boxs.forEach(box => {
        // a-tag within the box(p-tag)
        const link = box.querySelector("a");
        // if the link == current path
        if (link && link.getAttribute("href") === currentPath) {
            // add 'current' attribute
            box.classList.add("current");
            link.classList.add("current");
        } else {
            // remove 'current' attribute
            box.classList.remove("current");
        }
    });
});
const sidebarToggle = document.getElementById('sidebar-toggle');
const sidebar = document.querySelector('.sidebar');
const content = document.querySelector('.content');

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');

    if (sidebar.classList.contains('open')) {
        content.style.marginLeft = "var(--sidebar-width)";
    } else {
        content.style.marginLeft = "0";
    }
});
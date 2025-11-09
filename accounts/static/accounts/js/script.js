document.addEventListener("DOMContentLoaded", function () {
        const alertElement = document.getElementById("test_btn");
        

        if (alertElement) {
            const bsAlert = new bootstrap.Alert(alertElement);

            // Auto-close the alert after 5 seconds
            setTimeout(() => {
                bsAlert.close();
            }, 3000);
        }
    });

const toggleSidebar = document.getElementById('toggleSidebar');
const sidebar = document.getElementById('sidebar');

toggleSidebar.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    sidebar.classList.toggle('expanded');

    if (sidebar.classList.contains('expanded')){
        toggleSidebar.style.left = '190px';
    }else {
        toggleSidebar.style.left = '45px';
        console.log(toggleSidebar)
    }
});

// Highlight the active menu item dynamically
const links = document.querySelectorAll('#sidebar .nav-link');
links.forEach(link => {
    link.addEventListener('click', () => {
    // Remove active class from all links
    links.forEach(l => l.classList.remove('active'));
    // Add active class to the clicked link
    link.classList.add('active');
    });
});

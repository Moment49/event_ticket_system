document.addEventListener("DOMContentLoaded", function () {
        const alertElement = document.getElementById("test_btn");
        console.log(alertElement)

        if (alertElement) {
            const bsAlert = new bootstrap.Alert(alertElement);

            // Auto-close the alert after 5 seconds
            setTimeout(() => {
                bsAlert.close();
            }, 5000);
        }
    });

const toggleSidebar = document.getElementById('toggleSidebar');
const sidebar = document.getElementById('sidebar');

toggleSidebar.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    sidebar.classList.toggle('expanded');
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

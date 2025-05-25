 document.addEventListener('DOMContentLoaded', function() {
        const sidebar = document.getElementById('sidebar');
        const main = document.getElementById('main');
        const sidebarToggle = document.getElementById('sidebarToggle');
        const toggleIcon = sidebarToggle.querySelector('svg');

        // Check if sidebar state is saved in localStorage
        const isSidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (isSidebarCollapsed) {
            sidebar.classList.add('collapsed');
            main.classList.add('expanded');
            toggleIcon.style.transform = 'rotate(180deg)';
        }

        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            main.classList.toggle('expanded');

            // Save state to localStorage
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebarCollapsed', isCollapsed);

            // Rotate icon
            toggleIcon.style.transform = isCollapsed ? 'rotate(180deg)' : 'rotate(0)';
        });

        // Handle window resize
        function handleResize() {
            if (window.innerWidth <= 768) {
                sidebar.classList.add('collapsed');
                main.classList.add('expanded');
            } else {
                // Restore previous state on desktop
                const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
                sidebar.classList.toggle('collapsed', isCollapsed);
                main.classList.toggle('expanded', isCollapsed);
            }
        }

        window.addEventListener('resize', handleResize);
        handleResize(); // Initial check
    });
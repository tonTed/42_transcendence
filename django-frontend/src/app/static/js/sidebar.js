// display sections (using event delegation since the sidebar is loaded dynamically in index.html)
document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(event) {
        let header = event.target.closest('.section-header');
        
        if (header) {
            let content = header.nextElementSibling;
            
            if (content.style.display === 'block') {
                content.style.display = 'none';
                header.querySelector('div[id$="-section-arrow"]').innerHTML = '&#9654;';
            } else {
                content.style.display = 'block';
                header.querySelector('div[id$="-section-arrow"]').innerHTML = '&#9660;';
            }
        }
    });
});

// display account details (using event delegation since the sidebar is loaded dynamically in index.html)
document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(event) {
        let accountTrigger = event.target.closest('.account-user, .account-avatar, .account-infos');

        if (accountTrigger) {
            let detailsContainer = document.querySelector('.account-details-container');

            if (detailsContainer.style.display === 'block') {
                detailsContainer.style.display = 'none';
            } else {
                detailsContainer.style.display = 'block';
            }
        }
    });
});

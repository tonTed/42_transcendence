// Fetch and inject chat
function fetchChat() {
	fetch('/chat/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('.chat-container').innerHTML = data;
		})
		.catch(error => console.error('Error fetching chat', error));
};

function handleFriendListClick() {
    let title = document.getElementById('friend-list-title');
    title.onclick = function() {
        let content = document.getElementById('friend-list-content');
        let computedDisplay = window.getComputedStyle(content).getPropertyValue('display');
        if (computedDisplay === 'none') {
			document.getElementById('friend-list-title-arrow').innerHTML = "&#x25BC;";
            content.style.display = 'block';
        } else {
			document.getElementById('friend-list-title-arrow').innerHTML = "&#9654;";
			content.style.display = 'none';
        }
    };
}

// Show and hide friend requests list content
function handleFriendRequestsListClick() {
    let title = document.getElementById('friend-requests-list-title');
    title.onclick = function() {
        let content = document.getElementById('friend-requests-list-content');
        let computedDisplay = window.getComputedStyle(content).getPropertyValue('display');
        if (computedDisplay === 'none') {
			document.getElementById('friend-requests-list-title-arrow').innerHTML = "&#x25BC;";
            content.style.display = 'block';
        } else {
			document.getElementById('friend-requests-list-title-arrow').innerHTML = "&#9654;";
            content.style.display = 'none';
        }
    };
}

// Show and hide add friend list content
function handleAddFriendListClick() {
	let title = document.getElementById('add-friend-list-title');
    title.onclick = function() {
		let content = document.getElementById('add-friend-list-content');
        let computedDisplay = window.getComputedStyle(content).getPropertyValue('display');
        if (computedDisplay === 'none') {
			document.getElementById('add-friend-list-title-arrow').innerHTML = "&#x25BC;";
			content.style.display = 'block';
        } else {
			document.getElementById('add-friend-list-title-arrow').innerHTML = "&#9654;";
			content.style.display = 'none';
        }
    };
}

export { handleFriendRequestsListClick, handleFriendListClick, handleAddFriendListClick, fetchChat };

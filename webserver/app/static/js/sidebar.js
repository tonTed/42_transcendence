function handleFriendListClick() {
    const title = document.getElementById('friend-list-title');
    title.onclick = function() {
        const content = document.getElementById('friend-list-content');
        const computedDisplay = window.getComputedStyle(content).getPropertyValue('display');
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
    const title = document.getElementById('friend-requests-list-title');
    title.onclick = function() {
        const content = document.getElementById('friend-requests-list-content');
        const computedDisplay = window.getComputedStyle(content).getPropertyValue('display');
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
	const title = document.getElementById('add-friend-list-title');
    title.onclick = function() {
		const content = document.getElementById('add-friend-list-content');
        const computedDisplay = window.getComputedStyle(content).getPropertyValue('display');
        if (computedDisplay === 'none') {
			document.getElementById('add-friend-list-title-arrow').innerHTML = "&#x25BC;";
			content.style.display = 'block';
        } else {
			document.getElementById('add-friend-list-title-arrow').innerHTML = "&#9654;";
			content.style.display = 'none';
        }
    };
}

export { handleFriendRequestsListClick, handleFriendListClick, handleAddFriendListClick };

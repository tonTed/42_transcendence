// Show and hide friend list content
function handleFriendListClick() {
	let element = document.getElementById('friend-list-title');
    element.onclick = function() {
		console.log("friend list title clicked")
    };
}

// Show and hide friend requests list content
function handleFriendRequestsListClick() {
	let element = document.getElementById('friend-requests-list-title');
    element.onclick = function() {
		console.log("friend requests list title clicked")
    };
}

// Show and hide add friend list content
function handleAddFriendListClick() {
	let element = document.getElementById('add-friend-list-title');
    element.onclick = function() {
        console.log("add friend list title clicked")
    };
}

export { handleFriendListClick };
export { handleFriendRequestsListClick };
export { handleAddFriendListClick };
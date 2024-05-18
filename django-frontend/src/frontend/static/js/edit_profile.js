const updateUsername = async (newUsername) => {
    const url = `http://localhost:3000/api/users/updateUsername/${userId}/`;
    const csrfToken = document.getElementById('csrfToken').value;
    const data = {
        username: newUsername,
    };
    
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
            credentials: 'include'
        });

        if (response.ok) {
            const updatedUser = await response.json();
            console.log('Username updated successfully:', updatedUser);
        } else {
            console.error('Failed to update user:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

const updateAvatar = async (avatar) => {
    const url = `http://localhost:3000/api/users/updateAvatar/${userId}/`;
    const csrfToken = document.getElementById('csrfToken').value;
    // var image

    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: null,
            credentials: 'include'
        });

        if (response.ok) {
            const updatedUser = await response.json();
            console.log('User Avatar updated successfully:', updatedUser);
        } else {
            console.error('Failed to update user:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

export { updateUsername, updateAvatar };
const updateUsername = async (newUsername) => {
    const url = `http://localhost:3000/api/users/${userId}/`;
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
            console.log('User updated successfully:', updatedUser);
        } else {
            console.error('Failed to update user:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

export { updateUsername };
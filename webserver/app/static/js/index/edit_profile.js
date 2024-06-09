import { getCookie } from "../utils.js";

const updateUsername = async (newUsername) => {
    const userId = getCookie('id');
    const url = `api/users/updateUsername/${userId}/`;
    const csrfToken = getCookie('csrftoken');
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
    const userId = getCookie('id');
    const url = `api/users/updateAvatar/${userId}/`;
    const csrfToken = getCookie('csrftoken');
    const formData = new FormData();
    formData.append("avatar", avatar);

    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
            credentials: 'include'
        });

        if (response.ok) {
            const updatedUser = await response.json();
            console.log('Avatar updated successfully:', updatedUser);
            return updatedUser.avatar;
        } else {
            const errorData = await response.text();
            console.error('Failed to update avatar:', errorData);
            return null;
        }
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
};

export { updateUsername, updateAvatar };
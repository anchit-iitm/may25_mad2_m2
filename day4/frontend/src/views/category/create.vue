<template>
    <div class="Category-create">
        <h1>Create Category</h1>
            <div>
                <label for="name">Category Name:</label>
                <input type="text" id="name" v-model="this.categoryName" required>
            </div>
            <br>
            <div>
                <label for="description">Description:</label>
                <textarea id="description" v-model="this.categoryDescription" required></textarea>
            </div>
            <button v-on:click="this.addCategory()">Create Category</button>
    </div>
</template>
<script>
import axios from 'axios';
export default {
    name: 'CategoryCreate',
    data() {
        return {
            categoryName: '',
            categoryDescription: '',
            token: '',
        };
    },
    created() {
        this.token = localStorage.getItem('authToken');
        if (!this.token) {
            alert('You are not logged in. Please log in to create a category.');
            this.$router.push('/login');
        }
        if (localStorage.getItem('userRole') !== 'admin') {
            alert('You do not have permission to create a category.');
            this.$router.push({ name : 'home' });
        }
    },
    methods: {
        addCategory() {
            const categoryData = {
                name: this.categoryName,
                description: this.categoryDescription
            };
            axios.post('http://localhost:5000/category', categoryData, {
                headers: {
                    'Authorization': `${this.token}`
                }
            })
            .then(response => {
                if (response.status === 201) {
                    alert('Category created successfully!');
                    this.$router.push({ name : 'home' });
                } else {
                    alert('Failed to create category: ' + response.data.message);
                }
            })
            .catch(error => {
                alert('Error creating category: ' + error.message);
            });
        }
    }
};
</script>
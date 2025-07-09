<template>
    <div class="Category-edit">
        <h1>Edit Category</h1>
            <div>
                <label for="name">Category Name:</label>
                <input type="text" id="name" v-model="this.categoryName" required>
            </div>
            <br>
            <div>
                <label for="description">Description:</label>
                <textarea id="description" v-model="this.categoryDescription" required></textarea>
            </div>
            <button v-on:click="this.editCategory()">Edit Category</button>
    </div>
</template>
<script>
import axios from 'axios';
export default {
    name: 'CategoryEdit',
    data() {
        return {
            categoryName: '',
            categoryDescription: '',
            token: '',
            id: ''
        };
    },
    created() {
        this.id = this.$route.params.id;
        if (!this.id) {
            alert('Category ID is required to edit a category.');
            this.$router.push({ name : 'home' });
            return;
        }
        this.token = localStorage.getItem('authToken');
        if (!this.token) {
            alert('You are not logged in. Please log in to edit a category.');
            this.$router.push('/login');
        }
        if (localStorage.getItem('userRole') !== 'admin') {
            alert('You do not have permission to edit a category.');
            this.$router.push({ name : 'home' });
        }
        this.getCategory();
    },
    methods: {
        getCategory() {
            axios.get(`http://localhost:5000/category/${this.id}`, {
                headers: {
                    'Authorization': `${this.token}`
                }
            })
            .then(response => {
                if (response.status === 200) {
                    this.categoryName = response.data.data.name;
                    this.categoryDescription = response.data.data.description;
                } else {
                    alert('Failed to fetch category: ' + response.data.message);
                }
            })
            .catch(error => {
                alert('Error fetching category: ' + error.message);
            });
        },
        editCategory() {
            const categoryData = {
                name: this.categoryName,
                description: this.categoryDescription
            };
            axios.put(`http://localhost:5000/category/${this.id}`, categoryData, {
                headers: {
                    'Authorization': `${this.token}`
                }
            })
            .then(response => {
                if (response.status === 201) {
                    alert('Category edited successfully!');
                    this.$router.push({ name : 'home' });
                } else {
                    alert('Failed to edit category: ' + response.data.message);
                }
            })
            .catch(error => {
                alert('Error creating category: ' + error.message);
            });
        }
    }
};
</script>
<template>
    <div class="login-page">
        <h1>Login in to the app</h1>
        <div class="login-form">
            <span>Email: </span>
            <input type="email" placeholder="Enter your email" v-model="this.email" /><br><br>
            <span>Password: </span>
            <input id="password-field" type="password" placeholder="Enter your password" v-model="this.password" /><button v-on:click="this.togglePasswordVisibility()">!</button><br><br>
            <button v-on:click="this.login()">Login</button> | <button v-on:click="this.$router.push({name: 'register'})">Register</button>
        </div>
        <small>Single login page for all</small><br><br>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'LoginView',
    data(){
        return {
            email: '',
            password: '',
            message: ''
        }
    },
    methods: {
        togglePasswordVisibility() {
            const passwordInput = document.querySelector('input[id="password-field"]');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
            } else {
                passwordInput.type = 'password';
            }
        },
        login(){
            if (this.email === '' || this.password === '') {
                alert('Please fill in both fields.');
                return;
            }
            // axios.post().then().catch()
            // Example: Sending a POST request to a login endpoint
            axios
                .post('http://localhost:5000/auth/login',
                    {
                        email: this.email,
                        password: this.password
                    }
                )
                .then(Response => {
                    // Handle successful login response
                    // console.log('Login successful:', Response);
                    if (Response.status !== 200) {
                        alert('Login failed: ' + Response.data.message);
                        return;
                    }
                    if( Response.data.authToken === undefined || Response.data.authToken === null) {
                        alert('Login failed: ' + Response.data.message);
                        return;
                    }
                    localStorage.setItem('authToken', Response.data.authToken);
                    localStorage.setItem('userEmail', this.email);
                    localStorage.setItem('userID', Response.data.id);
                    localStorage.setItem('userRole', Response.data.role);
                    this.email = '';
                    this.password = '';
                    this.$router.push({name: 'home'});
                })
                .catch(error => {
                    // Handle error response
                    // console.error('Login failed:', error);
                    this.message = 'Login failed: ' + error.response.data.message;
                    alert(this.message);
                }); 
        }
    }
}
</script>
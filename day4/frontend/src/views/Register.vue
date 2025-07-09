<template>
    <div class="register-page">
        <h1>Regiser in to the app</h1>
        <div class="register-form">
            <span>Email: </span>
            <input type="email" placeholder="Enter your email" v-model="this.email" required/><br><br>
            <span>UserName: </span>
            <input type="text" placeholder="Enter your username" v-model="this.username" value="userName" required/><br><br>
            <span>Password: </span>
            <input id="password-field" type="password" placeholder="Enter your password" v-model="this.password" required/><button v-on:click="this.togglePasswordVisibility()">!</button><br><br>
            <button v-on:click="this.register()">Regiser</button> | <button v-on:click="this.$router.push({'name': 'login'})">Login</button>
        </div>
        <small>Single register page for all</small><br><br>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'RegiserView',
    data(){
        return {
            email: '',
            password: '',
            username: '',
            message: ''
        }
    },
    computed: {
        userName : function() {
            return this.email ? this.email.split('@')[0] : '';
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
        register(){
            if (this.email === '' || this.password === '' || this.username === '') {
                alert('Please fill in all fields.');
                return;
            }
            // axios.post().then().catch()
            // Example: Sending a POST request to a register endpoint
            axios
                .post('http://localhost:5000/auth/register',
                    {
                        email: this.email,
                        password: this.password,
                        username: this.username
                    }
                )
                .then(Response => {
                    // Handle successful register response
                    // console.log('Regiser successful:', Response);
                    if (Response.status !== 201) {
                        alert('Regiser failed: ' + Response.data.message);
                        return;
                    }

                    this.email = '';
                    this.password = '';
                    this.username = '';
                    alert('Regiser successful!');
                    // Optionally, redirect to login page
                    this.$router.push({ name: 'login' });
                })
                .catch(error => {
                    // Handle error response
                    // console.error('Regiser failed:', error);
                    if (error.response && error.response.data) {
                        alert('Regiser failed: ' + error.response.data.message);
                    } else {
                        alert('Regiser failed: ' + error.message);
                    }
                }); 
        }
    }
}
</script>
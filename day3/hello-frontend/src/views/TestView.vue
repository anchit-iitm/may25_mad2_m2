<template>
    <div class="test-view">
        <h1>Test View</h1>
        <TestComponent test_type="simple"/>
        <div class="test-form">
            <input type="text" placeholder="Enter some text" v-model="this.testMessage" />
            <button v-on:click="printMessage()">print it on the console</button>
        </div>
        <p>Test Message: {{ this.testMessage }}</p>
    </div>
</template>
<script>
import TestComponent from '@/components/TestComponent.vue'
export default {
    name: 'TestView',
    components:{
        TestComponent
    },
    data(){
        return {
            testMessage: ''
        }
    },
    methods: {
        printMessage() {
            console.log(this.testMessage);
        }
    }
}
</script>
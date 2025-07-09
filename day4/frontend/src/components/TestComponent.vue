<template>
    <div class="test-component">
        <p>This is a {{ test_type }} test view to demonstrate Vue.js component structure.</p>
        <p>Feel free to modify this content as needed.</p>
    </div>
</template>
<script>
export default {
    name: 'TestComponent',
    props: {
        test_type: {
            type: String,
            default: 'basic'
        }
    }
}
</script>
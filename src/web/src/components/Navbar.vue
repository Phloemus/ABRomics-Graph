<script setup>

    // Global state
    const isUserLoggedIn = useState('isUserLoggedIn')
    const userAuthToken = useState('userAuthToken')
    const isLoginPanelOpened = useState('isLoginPanelOpened')

    function displayLoginPanel() { 
        isLoginPanelOpened.value = true
    }

    function logout() {
        isUserLoggedIn.value = false
        userAuthToken.value = ""
    }

</script>

<template>
    <nav class="px-6 py-3 w-full bg-white border-b border-slate-200">
        <div class="flex flex-row-reverse gap-4">
            <ActionButton @click="displayLoginPanel" v-show="!isUserLoggedIn" content="Login"/>
            <SecondaryButton @click="logout" v-show="isUserLoggedIn" content="Log out"/>
        </div>
    </nav>
</template>

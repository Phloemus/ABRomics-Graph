<script setup>

    const isLoginPanelOpened = useState('isLoginPanelOpened', () => false)
    const isSidebarToggled = useState('isSidebarToggled', () => false)

</script>

<template>
    <div>
        <LoginPanel v-show="isLoginPanelOpened"/>
        <NuxtLayout>
            <NuxtPage/>
        </NuxtLayout>
    </div>
</template>

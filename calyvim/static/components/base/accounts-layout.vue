<script setup>
import BaseLayout from '@/components/base/base-layout.vue';
import CalyvimLogo from '@/assets/logo.png'
import { GithubOutlined, GoogleOutlined } from '@ant-design/icons-vue';

</script>

<template>
    <BaseLayout>
        <div
            class="min-h-screen flex items-center justify-center p-4 bg-[#F5F3FF] bg-gradient-to-br from-violet-50 to-violet-100">
            <a href="https://github.com/getcalyvim/calyvim" target="_blank" rel="noopener noreferrer"
                class="absolute top-4 right-4 inline-flex items-center gap-2 px-4 py-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 text-gray-700 hover:text-gray-900 text-xs no-underline">
                <GithubOutlined className="w-5 h-5" />
                <span>Star us on GitHub</span>
            </a>
            <div class="rounded-lg flex flex-col md:flex-row max-w-3xl w-full">
                <!-- Left side -->
                <div class="p-8 md:w-1/2 flex items-center justify-center">
                    <div class="text-center">
                        <div class="flex items-center gap-3 mb-3">
                            <img :src="CalyvimLogo" height="30" />
                            <div class="text-xl font-semibold text-gray-800">Calyvim Platform</div>
                        </div>
                        <p class="mt-1 text-gray-600">Catch the productivity wind.</p>
                    </div>
                </div>

                <!-- Right side -->
                <div class="md:w-1/2">

                    <div class="p-8 shadow-xl bg-white">
                        <slot></slot>
                    </div>
                </div>

                <!-- Bottom-left Status Button -->
                <a href="https://status.calyvim.com" target="_blank" rel="noopener noreferrer"
                    class="absolute bottom-4 left-4 inline-flex items-center gap-2 px-4 py-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 text-gray-700 hover:text-gray-900 text-xs no-underline">
                    <span>Status</span>
                </a>

                <!-- Bottom-right Contact Text -->
                <div class="absolute bottom-4 right-4 text-gray-600 text-xs">
                    <p>Need help? Contact us at <a href="mailto:hey@calyvim.in"
                            class="underline hover:text-gray-900">hey@calyvim.com</a></p>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>
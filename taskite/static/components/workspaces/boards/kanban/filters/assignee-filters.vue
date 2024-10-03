<script setup>
import { Avatar, Checkbox, CheckboxGroup } from 'ant-design-vue';
import { useKanbanStore } from '@/stores/kanban';
import { computed, ref } from 'vue';
import { generateAvatar } from '@/utils/helpers';

const store = useKanbanStore()
const showAllMembers = ref(false)

const visibleMembers = computed(() => {
    return showAllMembers.value ? store.members : store.members.slice(0, 5)
})

const toggleMemberVisibility = () => {
    showAllMembers.value = !showAllMembers.value
}
</script>

<template>
    <CheckboxGroup v-model:value="store.assigneeFilters" class="">
        <div class="flex flex-col gap-1">
            <div v-for="member in visibleMembers" :key="member.id" class="flex items-center gap-1">
                <Checkbox :value="member.id"></Checkbox>
                <Avatar size="small" :src="!!member.avatar ? member.avatar : generateAvatar(member.firstName)" />
                <div>{{ member.firstName }} {{ member?.lastName }}</div>
            </div>
            <div v-if="store.members.length > 5" class="mt-2">
                <a href="#" @click.prevent="toggleMemberVisibility">
                    {{ showAllMembers ? 'View less' : 'View more' }}
                </a>
            </div>
        </div>
    </CheckboxGroup>
</template>
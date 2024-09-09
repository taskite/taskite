<script setup>
import {
  CheckOutlined,
  CloseOutlined,
  WarningOutlined,
} from '@ant-design/icons-vue'
import { h } from 'vue'

const props = defineProps(['invites'])

const confirmInvite = (invite) => {
  window.location.href = invite.confirmationLink
}

const rejectInvite = (invite) => {
  window.location.href = invite.rejectionLink
}
</script>

<template>
  <a-card class="w-96" size="small">
    <div
      v-for="invite in props.invites"
      :key="invite.id"
      class="my-4"
      v-if="props.invites.length > 0"
    >
      <a-row :gutter="16">
        <a-col :span="12">
          <div class="text-xs">
            <span class="font-semibold"
              >{{ invite.invitedBy.firstName }}
              {{ invite.invitedBy?.lastName }}</span
            >
            invited you to join
            <span class="font-semibold italic">{{
              invite.workspace.name
            }}</span>
            workspace
          </div>
        </a-col>

        <a-col :span="12">
          <div class="flex items-center gap-3">
            <div>
              <a-button
                size="small"
                :icon="h(CheckOutlined)"
                type="text"
                @click="confirmInvite(invite)"
                >Accept</a-button
              >
            </div>

            <div>
              <a-button
                size="small"
                :icon="h(CloseOutlined)"
                type="text"
                @click="rejectInvite(invite)"
                >Reject</a-button
              >
            </div>
          </div>
        </a-col>
      </a-row>
    </div>

    <div v-else>
      <div class="flex justify-center">
        <WarningOutlined />
        <span class="ml-2">No invites present</span>
      </div>
    </div>
  </a-card>
</template>

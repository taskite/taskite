import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useOrganizationStore = defineStore('organization', () => {
  const organizations = ref([])

  const setOrganizations = (orgsData) => {
    organizations.value = orgsData
  }

  const allowedOrganizations = computed(() => {
    return organizations.value.filter(
      (organization) => ['admin', 'owner'].includes(organization.role)
    )
  })
  return { organizations, setOrganizations, allowedOrganizations }
})

<script setup>
import { useTheme } from 'vuetify'
import upgradeBannerDark from '@images/pro/upgrade-banner-dark.png'
import upgradeBannerLight from '@images/pro/upgrade-banner-light.png'
import VerticalNavLayout from '@layouts/components/VerticalNavLayout.vue'
import VerticalNavLink from '@layouts/components/VerticalNavLink.vue'
import VerticalNavSectionTitle from '@/@layouts/components/VerticalNavSectionTitle.vue'

// Components
import Footer from '@/layouts/components/Footer.vue'
import NavbarThemeSwitcher from '@/layouts/components/NavbarThemeSwitcher.vue'
import UserProfile from '@/layouts/components/UserProfile.vue'
import VerticalNavGroup from '@layouts/components/VerticalNavGroup.vue'

const vuetifyTheme = useTheme()

const upgradeBanner = computed(() => {
  return vuetifyTheme.global.name.value === 'light' ? upgradeBannerLight : upgradeBannerDark
})

const isCardDetailsVisible = ref(false)
</script>

<template>
  <VerticalNavLayout>
    <!-- 👉 navbar -->
    <template #navbar="{ toggleVerticalOverlayNavActive }">
      <div class="d-flex h-100 align-center">
        <!-- 👉 Vertical nav toggle in overlay mode -->
        <IconBtn
          class="ms-n3 d-lg-none"
          @click="toggleVerticalOverlayNavActive(true)"
        >
          <VIcon icon="mdi-menu" />
        </IconBtn>

        <!-- 👉 Search -->
        <div
          class="d-flex align-center cursor-pointer"
          style="user-select: none;"
        >
          <!-- 👉 Search Trigger button -->
          <IconBtn>
            <VIcon icon="mdi-magnify" />
          </IconBtn>

          <span class="d-none d-md-flex align-center text-disabled">
            <span class="me-3">Search</span>
            <span class="meta-key">&#8984;K</span>
          </span>
        </div>

        <VSpacer />

        <IconBtn
          class="me-2"
          href="https://github.com/hgalytoby/ACS"
          target="_blank"
          rel="noopener noreferrer"
        >
          <VIcon icon="mdi-github" />
        </IconBtn>

        <IconBtn class="me-2">
          <VIcon icon="mdi-bell-outline" />
        </IconBtn>

        <NavbarThemeSwitcher class="me-2" />

        <UserProfile />
      </div>
    </template>

    <template #vertical-nav-content>
      <VerticalNavLink
        :item="{
          title: 'Account Settings',
          icon: 'mdi-account-cog-outline',
          to: '/account-settings',
        }"
      />
      <VerticalNavGroup
        :item="{
          title: 'Settings',
          icon: 'mdi-cog-outline',
        }"
      >
        <VerticalNavLink
          :item="{
            title: 'UserList',
            icon: 'mdi-account-search-outline',
            to: '/user-list',
          }"
        />
        <VerticalNavLink
          :item="{
            title: 'UserLog',
            icon: 'mdi-book-open-variant',
            to: '/user-log',
          }"
        />
        <VerticalNavLink
          :item="{
            title: 'EmailLog',
            icon: 'mdi-email-search-outline',
            to: '/email-log',
          }"
        />
        <VerticalNavLink
          :item="{
            title: 'EmailMessage',
            icon: 'mdi-email-edit-outline',
            to: '/email-message',
          }"
        />
        <VerticalNavLink
          :item="{
            title: 'MemberLocationList',
            icon: 'mdi-map-marker-plus-outline',
            to: '/member-location-list',
          }"
        />
      </VerticalNavGroup>
      <!-- 👉 User Interface -->
      <VerticalNavSectionTitle
        :item="{
          heading: 'User Interface',
        }"
      />
      <VerticalNavLink
        :item="{
          title: 'Dashboard',
          icon: 'mdi-view-dashboard-outline',
          to: '/dashboard',
        }"
      />
      <VerticalNavLink
        :item="{
          title: 'Locations Overview',
          icon: 'mdi-map-marker-radius-outline',
          to: '/locations-overview',
        }"
      />
      <VerticalNavGroup
        :item="{
          title: 'Member',
          icon: 'mdi-account-multiple-outline',
        }"
      >
        <VerticalNavLink
          :item="{
            title: 'List',
            icon: 'mdi-account-group-outline',
            to: '/member-list',
          }"
        />
        <VerticalNavLink
          :item="{
            title: 'Create',
            icon: 'mdi-account-plus-outline',
            to: '/member-create',
          }"
        />
        <VerticalNavLink
          :item="{
            title: 'Record List',
            icon: 'mdi-book-account-outline',
            to: '/member-record-list',
          }"
        />
      </VerticalNavGroup>
      <VerticalNavLink
        :item="{
          title: 'Camera',
          icon: 'mdi-camera-marker-outline',
          to: '/camera',
        }"
      />
      <!-- 👉 User Interface -->
      <VerticalNavSectionTitle
        :item="{
          heading: '下面之後刪掉',
        }"
      />
      <VerticalNavLink
        :item="{
          title: 'Typography',
          icon: 'mdi-alpha-t-box-outline',
          to: '/typography',
        }"
      />
      <VerticalNavLink
        :item="{
          title: 'Icons',
          icon: 'mdi-eye-outline',
          to: '/icons',
        }"
      />
      <VerticalNavLink
        :item="{
          title: 'Tables',
          icon: 'mdi-table',
          to: '/tables',
        }"
      />
      <VerticalNavLink
        :item="{
          title: 'Cards',
          icon: 'mdi-credit-card-outline',
          to: '/cards',
        }"
      />
      <VerticalNavLink
        :item="{
          title: 'Form Layouts',
          icon: 'mdi-form-select',
          to: '/form-layouts',
        }"
      />
    </template>

    <!-- 👉 Pages -->
    <slot />

    <!-- 👉 Footer -->
    <template #footer>
      <Footer />
    </template>
  </VerticalNavLayout>
</template>

<style lang='scss' scoped>
.meta-key {
  border: thin solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 6px;
  block-size: 1.5625rem;
  line-height: 1.3125rem;
  padding-block: 0.125rem;
  padding-inline: 0.25rem;
}
</style>

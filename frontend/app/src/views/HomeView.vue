<template>
  <div class="bg-neutral-950 text-white min-h-screen flex flex-col">
    <Header />
    <main class="flex-1">
      <Hero />
      <SkillsBar />
      <Projects />
      <Experience />
      <Contacts />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Header from '@/components/landing/Header.vue'
import Hero from '@/components/landing/Hero.vue'
import SkillsBar from '@/components/landing/SkillsBar.vue'
import Projects from '@/components/landing/Projects.vue'
import Experience from '@/components/landing/Experience.vue'
import Contacts from '@/components/landing/Contacts.vue'
import Footer from '@/components/landing/Footer.vue'
</script>
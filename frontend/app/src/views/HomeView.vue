<template>
  <div class="landing">
    <ScrollProgress />
    <CursorGlow />
    <Header />
    <main>
      <Hero />
      <SkillsBar />
      <About />
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
import About from '@/components/landing/About.vue'
import Projects from '@/components/landing/Projects.vue'
import Experience from '@/components/landing/Experience.vue'
import Contacts from '@/components/landing/Contacts.vue'
import Footer from '@/components/landing/Footer.vue'
import ScrollProgress from '@/components/landing/effects/ScrollProgress.vue'
import CursorGlow from '@/components/landing/effects/CursorGlow.vue'
</script>

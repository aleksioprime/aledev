<template>
  <section class="min-h-screen flex flex-col items-center justify-center bg-neutral-900 text-neutral-100 px-4">
    <div
      class="flex flex-col items-center max-w-md w-full py-10 rounded-2xl shadow-2xl bg-neutral-800 animate-fade-in-up">
      <!-- SVG иконка или кастомный арт -->
      <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20 text-cyan-400 mb-6" fill="none" viewBox="0 0 24 24"
        stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.054 0 1.918-.816 1.995-1.85l.007-.15V6c0-1.054-.816-1.918-1.85-1.995L18.928 4H5.072c-1.054 0-1.918.816-1.995 1.85L3.07 6v12c0 1.054.816 1.918 1.85 1.995l.15.005z" />
      </svg>
      <h1 class="text-7xl font-extrabold text-cyan-400 mb-2 tracking-tight drop-shadow-xl">404</h1>
      <p class="text-2xl font-semibold mb-4">Страница не найдена</p>
      <router-link to="/"
        class="inline-block px-8 py-3 rounded-xl !bg-cyan-500 hover:!bg-cyan-400 transition font-bold shadow-lg text-neutral-900 text-lg">
        На главную
      </router-link>
    </div>
  </section>
</template>
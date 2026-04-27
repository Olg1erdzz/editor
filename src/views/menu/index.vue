<div class="relative group text-start font-medium rounded-lg text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20" id="dropdown-cta">
  <div
  role="button"
  class="flex items-center gap-1 rounded-lg  py-1 pr-4 text-start font-medium leading-tight text-gray-900 outline-none transition-all hover:bg-blue-gray-50 hover:bg-opacity-80 hover:text-blue-gray-900 focus:bg-blue-gray-50 focus:bg-opacity-80 focus:text-blue-gray-900 active:bg-blue-gray-50 active:bg-opacity-80 active:text-blue-gray-900"
>
  Ai Tools

</div>

<ul class="px-2 text-center rounded-lg hidden absolute bg-white z-10 w-40 border shadow-md divide-y group-hover:block" id="dropdown-items">
  
  <button class="w-full px-2 py-1 rounded-lg text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20"
  @click="getSelectedText"
  >
    简洁
  </button>
  <button class="w-full px-2 py-1 rounded-lg text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20">生动</button>
  <button class="w-full px-2 py-1 rounded-lg text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20">强烈</button>
  <button class="w-full px-2 py-1 rounded-lg text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20">委婉</button>
</ul>
</div>

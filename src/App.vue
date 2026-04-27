<template>
  <div id="app" v-cloak>
    <Home
      v-if="$route.meta.showNavbar"
      :documents="documents"
      :document="document"
      :editor="editor"
      @remove-document="removeDocument"
    />
    <main :class="{ 'with-navbar': $route.meta.showNavbar }">
      <router-view @add-document="addDocument" :documents="documents" :document="currentDocument" />
    </main>
  </div>
</template>

<script>
import Home from "@/components/Home.vue";

export default {
  name: "App",
  components: {
    Home
  },
  data() {
    return {
      editor: {
        type: Object,
        required: true
      },
      document: [],
      documents: [],
      currentDocument: null
    };
  },
  provide() {
    return {
      addDocument: this.addDocument,
      removeDocument: this.removeDocument
    };
  },
  methods: {
    addDocument(document) {
      const existingDocument = this.documents.find((doc) => doc.id === document.id);
      if (!existingDocument) {
        document.isOpen = true;
        this.documents.push(document);
        this.currentDocument = document;
      }
    },
    removeDocument({ id, index }) {
      const documentToRemove = this.documents.find((d) => d.id === id);
      if (documentToRemove) {
        documentToRemove.isOpen = false;
      }

      this.documents = this.documents.filter((doc) => doc.id !== id);
      if (!documentToRemove || this.$route.path !== documentToRemove.path) {
        return;
      }

      const previousDoc = this.documents[index - 1] || this.documents[0];
      if (previousDoc) {
        this.$router.push(previousDoc.path);
        this.currentDocument = previousDoc;
      } else {
        this.$router.push("/");
        this.currentDocument = null;
      }
    }
  }
};
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.with-navbar {
  margin-top: 4rem;
}

body,
html {
  height: 100%;
  margin: 0;
  padding: 0;
  background: #f6f7f9;
}
</style>

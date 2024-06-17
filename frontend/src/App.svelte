<script>
  import Router from "svelte-spa-router";

  import Main from "./routes/Main/Main.svelte";
  import UploadFiles from "./routes/UploadFiles/UploadFiles.svelte";
  import Setting from "./routes/Setting/Setting.svelte";
  import BoxTest from "./routes/BoxTest/BoxTest.svelte";

  const routes = {
    '/': Main,
    '/uploadfiles': UploadFiles,
    '/setting': Setting,
    '/boxtest': BoxTest,
  }
</script>

<Router {routes}/>
<script>
  import Router from "svelte-spa-router";

  import Main from "./routes/Main/Main.svelte";
  import UploadFiles from "./routes/UploadFiles/UploadFiles.svelte";
  import Setting from "./routes/Setting/Setting.svelte";

  const routes = {
    '/': Main,
    '/uploadfiles': UploadFiles,
    '/setting': Setting,
  }
</script>

<Router {routes}/>
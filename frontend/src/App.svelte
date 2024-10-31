<script>
  import Router from "svelte-spa-router";

  // 페이지 불러오가
  import Main from "./routes/Main/Main.svelte";
  import UploadFiles from "./routes/UploadFiles/UploadFiles.svelte";
  import MakeJson from "./routes/MakeJson/MakeJson.svelte";

  // 페에지 연결
  const routes = {
    "/": Main,
    "/uploadfiles": UploadFiles,
    "/makejson": MakeJson,
  };
</script>

<!-- 라우터 연결 -->
<Router {routes} />

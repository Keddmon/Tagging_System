<script>
    import { push } from "svelte-spa-router";
    import "./Main.css";

    const goToUploadFiles = () => {
        push("/uploadfiles");
    }
</script>

<!-- <div class="main-container"> -->
    <div class="main-wrap">
        <div class="main-infos-wrap">
            <div class="main-title-wrap">
                <span>YOLOv8을 활용한 패션 이미지 데이터 어노테이션 시스템</span>
            </div>
            <div class="main-info-wrap">
                <span>본 시스템은 대량의 패션 이미지에 대해 데이터 어노테이션(레이블링)을 목적으로 합니다.</span>
                <span>또한, 생성되는 어노테이션 데이터는 TXT-YOLO(You Only Look Once) 포맷을 따릅니다.</span>
            </div>
            <div class="main-data-wrap">
                <div class="main-data-title">
                    <span>필요한 데이터</span>
                </div>
                <div class="main-data-info">
                    <span>원본 이미지 : .jpg or .png </span>
                    <span>카테고리 데이터 : .json </span>
                </div>
            </div>
        </div>
        <div class="main-btn-wrap">
            <button on:click={goToUploadFiles}>시작하기</button>
        </div>
    </div>
<!-- </div> -->

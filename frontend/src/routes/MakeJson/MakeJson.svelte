<script>
    import { push } from "svelte-spa-router";
    import "./MakeJson.css";

    let imageName = "";
    let topCategory = "";
    let bottomCategory = "";

    const goBack = () => {
        push('/uploadfiles');
    };

    const makeJson = async () => {
        try {

            const makeJsonRes = await fetch(
                "http://127.0.0.1:8000/api/makejson/make-json",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        image_name: imageName,
                        top_category: topCategory,
                        bottom_category: bottomCategory,
                    }),
                },
            );

            if (!makeJsonRes.ok) {
                throw new Error("Network Error");
            }

            alert("성공");
        } catch (error) {
            alert("ERROR");
        }
    };
</script>

<div class="boxtest-container">
    <div class="boxtest-title-box">
        <span class="boxtest-title">
            테스트할 이미지 내 아이템 카테고리를 입력해 주세요.
        </span>
    </div>
    <div class="boxtest-name-input">
        <span class="input-tag">이미지명</span>
        <input type="text" bind:value={imageName} />
    </div>
    <div class="boxtest-top-input">
        <span class="input-tag">상의</span>
        <input type="text" bind:value={topCategory} />
    </div>
    <div class="boxtest-bottom-input">
        <span class="input-tag">하의</span>
        <input type="text" bind:value={bottomCategory} />
    </div>
    <span> 입력된 내용은 JSON으로 저장됩니다. </span>
    <div class="boxtest-btn-box">
        <button on:click={makeJson}> 확인 </button>
        <button on:click={goBack}>뒤로가기</button>
    </div>
</div>

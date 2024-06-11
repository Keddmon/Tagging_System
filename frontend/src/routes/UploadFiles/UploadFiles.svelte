<script>
    import { push } from "svelte-spa-router";
    import "./UploadFiles.css";
    import system_concept from "./system_concept.png";

    // 전역 변수로 JSON 파일 경로 저장
    let jsonLocations = [];

    /**
     * 뒤로가기
     */
    const goBack = () => {
        push("/");
    };

    /**
     * setting으로 이동
     */
    const goSetting = () => {
        push("/setting");
    };

    /**
     * 이미지 및 텍스트 파일 업로드
     */
    const uploadFiles = async (event) => {
        try {
            const imageFiles = document.getElementById("imageInput").files;
            const jsonFiles = document.getElementById("jsonInput").files;

            if (imageFiles.length !== jsonFiles.length) {
                alert("이미지 파일과 JSON 파일의 수가 동일해야 합니다.");
            }

            const formData = new FormData();

            for (let i = 0; i < imageFiles.length; i++) {
                formData.append("images", imageFiles[i]);
                formData.append("jsons", jsonFiles[i]);
            }

            const uploadFiles = await fetch(
                "http://127.0.0.1:8000/api/uploadfiles/upload-files",
                {
                    method: "POST",
                    body: formData,
                },
            );

            if (!uploadFiles.ok) {
                console.error("Error: ", uploadFiles.statusText);
                isUpload.set(false);
                return;
            }

            const uploadFilesData = await uploadFiles.json();
            const json_locations = uploadFilesData.json_locations;
            console.log("upload_files API 호출 성공");

            for (let i = 0; i < json_locations.length; i++) {
                jsonLocations.push(json_locations[i]);
            }

            alert("업로드가 완료되었습니다.");
        } catch (error) {
            alert("업로드에 실패하였습니다.");
        }
    };

    /**
     * API 통합
     */
    const testAPI = async () => {
        try {
            /**
             * 폴더 생성 API (setup_directories API)
             */
            const setupDirs = await fetch(
                "http://127.0.0.1:8000/api/setupdirs/setup-dirs",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                },
            );
            if (!setupDirs.ok) {
                throw new Error("setup_directories API 호출 실패");
            }

            const setupDirsData = await setupDirs.json();
            console.log("setup_directories API 호출 성공");

            /**
             * 이미지 복사 API (copy_images API)
             */
            const copyImages = await fetch(
                "http://127.0.0.1:8000/api/copyimages/copy-images",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        dir: setupDirsData.target_dir,
                    }),
                },
            );
            if (!copyImages.ok) {
                throw new Error("copy_images API 호출 실패");
            }

            const copyImagesData = await copyImages.json();
            console.log(copyImagesData, "copy_images API 호출 성공");

            /**
             * 클래스 라벨링 API (class_labeling API)
             */
            const classLabeling = await fetch(
                "http://127.0.0.1:8000/api/classlabeling/class-labeling",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        // images_dir: setupDirsData.images_dir,
                        // labels_dir: setupDirsData.labels_dir,
                        // 임시 테스트용 ######################################
                        images_dir: setupDirsData.original_images_dir,
                        labels_dir: setupDirsData.original_labels_dir,
                        failed_images_dir: setupDirsData.failed_images_dir,
                        // #################################################
                        image_files: copyImagesData.image_files,
                        json_files: jsonLocations,
                    }),
                },
            );

            if (!classLabeling.ok) {
                throw new Error("class_labeling API 호출 실패");
            }

            const classLabelingData = await classLabeling.json();
            console.log(classLabelingData.class_mapping);

            /**
             * classes.txt 및 dataset.yaml API (label_data API)
             */
            const labeldata = await fetch(
                "http://127.0.0.1:8000/api/labeldata/label-data",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        target_dir: setupDirsData.target_dir,
                        // labels_dir: setupDirsData.labels_dir,
                        // images_dir: setupDirsData.images_dir,
                        // 임시 테스트용 ######################################
                        images_dir: setupDirsData.original_images_dir,
                        labels_dir: setupDirsData.original_labels_dir,
                        class_mapping: classLabelingData.class_mapping,
                    }),
                },
            );
            if (!labeldata.ok) {
                throw new Error("label_data API 호출 실패");
            }

            console.log("통합 API 호출 성공");
            alert("어노테이션 데이터 생성 완료.");
        } catch (error) {
            alert("ERROR");
            console.log("API 통합 에러: ", error);
        }
    };
</script>

<div class="uploadfiles-container">
    <div class="uploadfiles-wrap">
        <div class="uploadfiles-input-wrap">
            <div class="input-files-wrap">
                <span>이미지 파일 첨부</span>
                <input id="imageInput" type="file" accept="image/*" multiple />
            </div>
            <div class="input-files-wrap">
                <span>JSON 파일 첨부</span>
                <input id="jsonInput" type="file" accept=".json" multiple />
            </div>
        </div>
        <div class="input-btn-wrap">
            <button on:click={uploadFiles}>업로드</button>
        </div>
    </div>
    <div class="uploadfiles-btn-wrap">
        <button on:click={testAPI}>실행</button>
    </div>
    <div class="system-info-wrap">
        <span class="system-info-title">
            본 시스템은 아래와 같은 과정을 따릅니다.
        </span>
        <span> 1. 이미지 및 카테고리 JSON 업로드 </span>
        <div class="system-info-with-etc">
            <span> 2. 포맷 폴더 생성 </span>
            <span class="system-info-etc">
                - new_label_data / images, failed_images, labels, train, valid,
                test
            </span>
        </div>
        <span> 3. 객체 탐지 후 JSON 클래스 매칭 및 좌표 정규화 </span>
        <div class="system-info-with-etc">
            <span> 4. 부가 데이터 파일 생성 </span>
            <span class="system-info-etc"> - dataset.yaml, classes.txt </span>
        </div>
    </div>
    <div class="system-concept-wrap">
        <span class="system-concept-title">개념도</span>
        <img
            src={system_concept}
            alt="system_concept"
            width="100%"
            height="100%"
        />
    </div>
</div>

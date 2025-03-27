document.addEventListener("DOMContentLoaded", function() {
    let imageUpload = document.getElementById("fruit360-imageUpload");
    let uploadedImage = document.getElementById("fruit360-uploadedImage");
    let loadingSpinner = document.getElementById("fruit360-loading");
    let resultTable = document.getElementById("fruit360-resultTable");

    // Xử lý tải và hiển thị ảnh
    imageUpload.addEventListener("change", function() {
        let file = this.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = function(e) {
                uploadedImage.src = e.target.result;
                uploadedImage.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });

    // Gửi ảnh lên server để nhận diện
    window.fruit360UploadImage = function() {
        let fileInput = imageUpload.files[0];
        if (!fileInput) {
            alert("Vui lòng chọn ảnh!");
            return;
        }

        let formData = new FormData();
        formData.append("file", fileInput);

        // Hiển thị loading spinner
        loadingSpinner.style.display = "block";
        resultTable.style.display = "none";

        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingSpinner.style.display = "none";

            if (data.error) {
                alert("Lỗi: " + data.error);
                console.error("Lỗi:", data.error);
            } else {
                let tbody = document.querySelector("#fruit360-resultTable tbody");
                tbody.innerHTML = "";
                data.predictions.forEach((item, index) => {
                    let row = tbody.insertRow();
                    row.insertCell(0).innerText = index + 1;
                    row.insertCell(1).innerText = item.label;
                    row.insertCell(2).innerText = (item.confidence * 100).toFixed(2) + "%";
                });
                resultTable.style.display = "block";
            }
        })
        .catch(error => {
            loadingSpinner.style.display = "none";
            alert("Có lỗi xảy ra khi nhận diện!");
            console.error("Lỗi:", error);
        });
    };
});